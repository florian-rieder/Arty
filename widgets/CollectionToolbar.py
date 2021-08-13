from types import BuiltinFunctionType
from plyer import filechooser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
import kivy.properties as kyprops
from kivymd.uix.menu import MDDropdownMenu

from widgets.PopupMessage import PopupMessage
from widgets.FilterPopup import FilterPopup
from widgets.ConfirmationSnackbar import ConfirmationSnackbar
from api.Collection import CollectionUtils, CollectionManager
from api.Powerpoint import Powerpoint

class CollectionToolbar(BoxLayout):
    """ Summary
        -------
        Toolbar to access other pages (Comparison).

        Attributes
        ----------
        selected_images: ListProperty
            List of the selected images
        save_destination: ListProperty

        displayed_images: ListProperty
            List of the current displayed images
        sorting_attributes: ListProperty
            List of the sorting attributes
        title_filter: StringProperty
            Current title in filter
        artist_filter: StringProperty
            Current artist in filter
        technique_filter: StringProperty
            Current technique in filter
        mode_filter: StringProperty
            Current filter mode
        mode_text_filter: StringProperty
            Current filter mode name

        Methods
        -------
        to_home_screen()
            on_press home button, return to the start screen
        save_coll()
            on_press save button, saves the current collection
        select_all()
            on_press select all button, select all the images of the collection
        compare()
            on_press compare button, switches to ComparisonScreen and
            send selected images
        export()
            on_press export button, exports selection to pptx
        sort_by()
            on_press sort by button, sorts the collection
        open_filter()
            on_press filter button, opens the filter window

    """
    Builder.load_file('templates/CollectionToolbar.kv')

    selected_images = kyprops.ListProperty(list())
    displayed_images = kyprops.ListProperty(list())
    sorting_attributes = kyprops.ListProperty(
                            ['Title [A-Z]', 'Title [Z-A]',
                            'Artist [A-Z]','Artist [Z-A]',
                            'Datation Increasing','Datation Decreasing']
                            )
    title_filter = kyprops.StringProperty('')
    artist_filter = kyprops.StringProperty('')
    style_filter = kyprops.StringProperty('')
    technique_filter = kyprops.StringProperty('')
    mode_filter = kyprops.StringProperty('normal')
    mode_text_filter = kyprops.StringProperty('and')

    # NOT WORKING
    # toolbar_icon = kyprops.ListProperty([
    #     ["sort-ascending", lambda x: open_filter(), 'Sort the collection'],
    #     ['filter-variant', lambda x:open_filter(), 'Filter the images'],
    #     ['check-all', lambda x: select_all(), 'Select all the images, Ctrl+A'],
    #     ["content-save", lambda x: save_coll(), 'Save the collection, Ctrl+S'],
    #     ['compare', lambda x: compare(), 'Compare the selected images'],
    #     ["microsoft-powerpoint", lambda x: export(), 'Create a .pptx with selected images, Ctrl+E']
    #     ]
    # )
    def build_sort_drop(self):
        sort_items = [
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-alphabetical-ascending',
            'text': 'Title [A-Z]',
            'on_release': lambda x = 'Title [A-Z]': self.sort_by(x)},
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-alphabetical-descending',
            'text': 'Title [Z-A]',
            'on_release': lambda x = 'Title [Z-A]': self.sort_by(x)},
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-alphabetical-ascending',
            'text': 'Artist [A-Z]',
            'on_release': lambda x = 'Artist [A-Z]': self.sort_by(x)},
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-alphabetical-descending',
            'text': 'Artist [Z-A]',
            'on_release': lambda x = 'Artist [Z-A]': self.sort_by(x)},
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-numerical-ascending',
            'text': 'Datation Increasing',
            'on_release': lambda x = 'Datation Increasing': self.sort_by(x)},
            {'viewclass': 'OneLineListItem',
            'icon': 'sort-numerical-descending',
            'text': 'Datation Decreasing',
            'on_release': lambda x = 'Datation Decreasing': self.sort_by(x)}
            ]

        self.sort_menu = MDDropdownMenu(
            items= sort_items,
            width_mult= 3,
            position= 'bottom',
            max_height= 300
        )
        return self.sort_menu
    
    def sort_drop(self, button):
        self.menu = self.build_sort_drop()

        self.menu.caller = button
        self.menu.open()

    def to_home_screen(self):
        """ Summary
            -------
            Returns to the start screen
        """
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION

        # switches to start screen
        CollectionManager.save(collection)
        app.SCREEN_MANAGER.switch_to(app.SCREENS["START"], direction ='right')

    def save_coll(self):
        """ Summary
            -------
            Saves the current collection
        """
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION

        # saves curent collection
        CollectionManager().save(collection)
        ConfirmationSnackbar().open()



    def select_all(self):
        """ Summary
            -------
            Selects all the images from the collection
        """

        app = App.get_running_app()

        # select all images if not all images are selected, or deselect
        # all images if all images are already selected.
        do_select = self.selected_images != self.displayed_images

        # activate checkboxes
        for grid_image in app.GRID.children:
            grid_image.ids.select_image.active = do_select

        # update selected_images
        if do_select:
            self.selected_images = self.displayed_images
        else:
            self.selected_images = list()


    def compare(self):
        """ Summary
            -------
            Opens the comparaison screen fi 2 to 4 images are selected
        """
        # get selected images
        # send them to the compare screen
        try:
            app = App.get_running_app()
            app.SCREENS["COMPARE"].load_images(self.selected_images)
            app.SCREEN_MANAGER.switch_to(
                app.SCREENS["COMPARE"],
                direction ='left')
        except ValueError:
            #show popup if the wrong amount of images is selected
            PopupMessage(message = "Please select 2 to 4 images").open()


    def sort_by(self, value):
        """ Summary
            -------
            Sorts the collection with the selected paramter
        """
        app = App.get_running_app()

        # sorts the whole collection if it is the displayed one
        if len(self.displayed_images) == 0:
            self.displayed_images = app.CURRENT_COLLECTION.get_collection()

        val_to_sort = value.split()
        reverse = True
        # checks sorting order
        if val_to_sort[1] in ('[A-Z]', 'Increasing'):
            reverse = False

        # sort the image list
        self.displayed_images = CollectionUtils.sort(
                                        self.displayed_images,
                                        val_to_sort[0].lower(),
                                        reverse=reverse
                                        )

        # sets the grid with the sorted collection
        app.GRID.set_display_list(self.displayed_images)
        self.selected_images = list()


    def open_filter(self):
        """ Summary
            -------
            Opens the filter window with the current filters
        """

        # opens the filter class with saved inputs
        FilterPopup(
            title_art = self.title_filter,
            artist = self.artist_filter,
            style = self.style_filter,
            technique = self.technique_filter,
            mode = self.mode_filter,
            mode_text = self.mode_text_filter
        ).open()


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
                filters=["*.pptx"], # FIXME: crashes on replace existing file...
                use_extensions=True
            )

        except Exception:
            Logger.exception(
                "An error occurred when selecting save destination"
            )
            PopupMessage(
                message = "An error occurred when selecting save destination"
            ).open()


    def handle_selection(self, selection):
        """
        Callback function for handling the selection response from Activity.
        """
        # 2. generate the powerpoint and save it to the selected path
        export_path = str(selection[0])
        app = App.get_running_app()

        Logger.info("Arty: exporting selection to pptx...")
        ConfirmationSnackbar(text="Exporting to PowerPoint...").open()

        try:
            Powerpoint.create_presentation(
                self.selected_images,
                app.PROJECT_DIRECTORY,
                export_path
            )
        except Exception as exc:
            Logger.exception(exc)
            PopupMessage(
                message="An error occurred while generating the presentation"
            ).open()
