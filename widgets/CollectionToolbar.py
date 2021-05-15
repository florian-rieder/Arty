import collections
from plyer import filechooser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
import kivy.properties as kyprops

from widgets.PopupMessage import PopupMessage
from widgets.FilterDropdown import FilterDropdown
from api.Collection import CollectionUtils
from api.Collection import CollectionManager
from api.Powerpoint import Powerpoint

class CollectionToolbar(BoxLayout):
    """ Summary
        -------
        Toolbar to access other pages (Comparison).

        Attributes
        ----------
        selected_images
        save_destination

        Methods
        -------
        compare()
            on_press compare button, switches to ComparisonScreen and
            send selected images
        export()
            on_press export button, exports selection to pptx

        TODO
        ----
        Remember the list of currently displayed images
    """
    Builder.load_file('templates/CollectionToolbar.kv')

    selected_images = kyprops.ListProperty(list())
    save_destination = kyprops.ListProperty(list())
    displayed_images = kyprops.ListProperty(list())
    sorting_attributes = kyprops.ListProperty(
                            ['Title [A-Z]', 'Title [Z-A]',
                            'Artist [A-Z]','Artist [Z-A]',
                            'Datation Increasing','Datation Decreasing']
                            )
    
    def to_home_screen(self):
        """
            TODO: docstring
        """
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION
        
        CollectionManager.save(collection)
        app.SCREEN_MANAGER.switch_to(app.SCREENS["START"], direction ='right')

    def save_coll(self):
        """
            TODO: docstring
        """
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION
        CollectionManager().save(collection)

    def compare(self):
        """
            TODO: docstring
        """
        # get selected images
        # send them to the compare screen
        try:
            app = App.get_running_app()
            app.SCREENS["COMPARE"].load_images(self.selected_images)
            app.SCREEN_MANAGER.switch_to(app.SCREENS["COMPARE"], direction ='left')
        except Exception:
            #show popup if the wrong amount of images is selected
            PopupMessage(message = "Please select 2 to 4 images").open()
            # popup_content = PopupMessage(message = "Please select 2 to 4 images")
            # popup_window = Popup(
            #     title = "Error",
            #     content = popup_content,
            #     size_hint = (0.3, 0.25)
            # )

            # popup_content.ids.popup_btn.bind(on_press = popup_window.dismiss)

            # popup_window.open()

    def export(self):
        """
            Call plyer filechooser API to run a filechooser Activity.
        """
        if len(self.selected_images) == 0:
            PopupMessage(message="Please select at least one image").open()
            return
        # 1. select a file to save to
        try:
            filechooser.save_file(
                on_selection=self.handle_selection,
                #filters=["*pptx"] # crashes on replace existing file...
            )
        except Exception:
            Logger.exception(
                "An error occurred when selecting save destination"
            )
            PopupMessage(
                message = "An error occurred when selecting save destination"
            ).open()


    def sort_by(self, value):
        """
            TODO: docstring
        """
        # TODO: replace with CollectionToolbar current image list
        
        app = App.get_running_app()
        
        if len(self.displayed_images) == 0:
            self.displayed_images = app.CURRENT_COLLECTION.get_collection()
        
        val_to_sort = value.split()
        # sort the image list
        if val_to_sort[1] == '[A-Z]' or 'Increasing':
            print(val_to_sort[1])
            self.displayed_images = CollectionUtils.sort(
                                            self.displayed_images,
                                            val_to_sort[0].lower()
                                            )
        else:
            print(val_to_sort[1])
            self.displayed_images = CollectionUtils.sort(
                                            self.displayed_images,
                                            val_to_sort[0].lower(),
                                            reverse= True
                                            )
        app.GRID.set_display_list(self.displayed_images)

    def open_filter(self):
        """
            TODO: docstring
        """
        filter_dropdown = FilterDropdown()
        mainbutton = self.ids.filter_select

        mainbutton.bind(on_press = filter_dropdown.open)

        filter_dropdown.ids.filter_btn.bind(on_release = filter_dropdown.dismiss)

    def handle_selection(self, selection):
        """
        Callback function for handling the selection response from Activity.
        """
        # 2. generate the powerpoint and save it to the selected path
        path = str(selection[0])
        app = App.get_running_app()
        Logger.info("Arty: exporting selection to pptx")
        Powerpoint.create_presentation(self.selected_images, app.PROJECT_DIRECTORY, path)
