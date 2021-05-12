from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.logger import Logger
import kivy.properties as kyprops
from plyer import filechooser

from widgets.PopupMessage import PopupMessage
from widgets.FilterDropdown import FilterDropdown
from api.Collection import CollectionImage, Collection
from api.Powerpoint import Powerpoint

class CollectionToolbar(BoxLayout):
    """ Summary
        -------
        Toolbar to access other pages (Comparison).

        Attributes
        ----------

        Methods
        -------
        compare()
            on_press compare button, switches to ComparisonScreen and
            send selected images
        export()
            on_press export button, exports selection to pptx

    """
    Builder.load_file('templates/CollectionToolbar.kv')

    selected_images = kyprops.ListProperty(list())
    save_destination = kyprops.ListProperty(list())

    def compare(self):
        # get selected images
        # send them to the compare screen

        try:
            app = App.get_running_app()
            app.SCREENS["COMPARE"].load_images(self.selected_images)
            app.SCREEN_MANAGER.switch_to(app.SCREENS["COMPARE"], direction ='left')
        except Exception:
            Logger.exception("Please select 2 to 4 images")
            
            #show popup if the wrong amount of images is selected
            popup_content = PopupMessage(message = "Please select 2 to 4 images")
            popup_window = Popup(
                title = "Error",
                content = popup_content,
                size_hint = (0.3, 0.25)
            )

            popup_content.ids.popup_btn.bind(on_press = popup_window.dismiss)

            popup_window.open()

    def export(self):
        """
        Call plyer filechooser API to run a filechooser Activity.
        """
        # 1. select a file to save to
        try:
            filechooser.save_file(
                on_selection=self.handle_selection,
                #filters=["*pptx"] # crashes on replace existing file...
            )
        except Exception:
            Logger.exception("An error occurred when selecting save destination")
    
    def sorting_by(self, value):
        app = App.get_running_app()
        sorted_coll = app.CURRENT_COLLECTION.sort(value)
        app.GRID.set_display_list(sorted_coll)
    
    def open_filter(self):

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
