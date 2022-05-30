from types import BuiltinFunctionType
from plyer import filechooser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.metrics import dp
import kivy.properties as kyprops

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
#from kivymd.uix.textfield import MDTextField

from widgets.FilterDialogContent import FilterDialogContent
from widgets.ExportDialogContent import ExportDialogContent
from widgets.ToggleButtonWidget import ToggleButtonWidget
from widgets.ConfirmationSnackbar import ConfirmationSnackbar
from widgets.IconListItem import IconListItem
from api.CollectionUtils import CollectionUtils
from api.CollectionManager import CollectionManager
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

    app = None

    selected_images = kyprops.ListProperty(list())
    displayed_images = kyprops.ListProperty(list())

    # reference to the dialog currently being displayed. None if no
    # dialog is active

    dialog = None
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

    def __init__(self, **kwargs):
        super(CollectionToolbar, self).__init__(**kwargs)
        self.app = App.get_running_app()
    
    def sort_drop(self, button):
        sort_items = [
            {'viewclass': 'IconListItem',
            'icon': 'order-alphabetical-ascending',
            'text': 'Title',
            'on_release': lambda x = 'title': self.sort_by(x, rev=False)},
            {'viewclass': 'IconListItem',
            'icon': 'order-alphabetical-descending',
            'text': 'Title',
            'on_release': lambda x = 'title': self.sort_by(x, rev=True)},
            {'viewclass': 'IconListItem',
            'icon': 'order-alphabetical-ascending',
            'text': 'Artist',
            'on_release': lambda x = 'artist': self.sort_by(x, rev=False)},
            {'viewclass': 'IconListItem',
            'icon': 'order-alphabetical-descending',
            'text': 'Artist',
            'on_release': lambda x = 'artist': self.sort_by(x, rev=True)},
            {'viewclass': 'IconListItem',
            'icon': 'order-numeric-ascending',
            'text': 'Date',
            'on_release': lambda x = 'datation': self.sort_by(x, rev=False)},
            {'viewclass': 'IconListItem',
            'icon': 'order-numeric-descending',
            'text': 'Date',
            'on_release': lambda x = 'datation': self.sort_by(x, rev=True)}
            ]

        self.sort_menu = MDDropdownMenu(
            items= sort_items,
            width_mult= 2.5,
            position= 'bottom',
            max_height= dp(300),
            ver_growth= 'down'
        )

        self.sort_menu.caller = button
        self.sort_menu.open()

    def to_home_screen(self):
        """ Summary
            -------
            Returns to the start screen
        """
        collection = self.app.CURRENT_COLLECTION

        # switches to start screen
        CollectionManager.save(collection)
        self.app.SCREEN_MANAGER.switch_to(self.app.SCREENS["START"], direction ='right')

    def save_coll(self):
        """ Summary
            -------
            Saves the current collection
        """
        collection = self.app.CURRENT_COLLECTION

        # saves curent collection
        CollectionManager().save(collection)
        ConfirmationSnackbar().open()



    def select_all(self):
        """ Summary
            -------
            Selects all the images from the collection
        """

        # select all images if not all images are selected, or deselect
        # all images if all images are already selected.
        do_select = self.selected_images != self.displayed_images

        # activate checkboxes
        for grid_image in self.app.GRID.children:
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
            self.app.SCREENS["COMPARE"].load_images(self.selected_images)
            self.app.SCREEN_MANAGER.switch_to(
                self.app.SCREENS["COMPARE"],
                direction ='left')
        except ValueError:
            #show popup if the wrong amount of images is selected
            self.app.show_error(message = "Please select 2 to 4 images")


    def sort_by(self, value, rev):
        """ Summary
            -------
            Sorts the collection with the selected paramter
        """
        # sorts the whole collection if it is the displayed one
        # if len(self.displayed_images) == 0:
        #     self.displayed_images = self.app.CURRENT_COLLECTION.get_collection()

        # val_to_sort = value.split()
        # reverse = True
        # # checks sorting order
        # if val_to_sort[1] in ('[A-Z]', 'Increasing'):
        #     reverse = False

        # sort the image list
        self.displayed_images = CollectionUtils.sort(
                                        self.displayed_images,
                                        value,
                                        reverse=rev
                                        )

        # sets the grid with the sorted collection
        self.app.GRID.set_display_list(self.displayed_images)
        self.selected_images = list()


    def open_filter(self):
        """ Summary
            -------
            Opens the filter window with the current filters
        """

        if not self.dialog:
            self.dialog = MDDialog(
                title="Filter",
                type="custom",
                content_cls=FilterDialogContent(),
                buttons=[
                    MDRaisedButton(
                        text="FILTER",
                        on_release=self.filter
                    ),
                    MDRaisedButton(
                        text="RESET",
                        on_release=self.reset_filter
                    ),
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=self.dismiss_dialog
                    ),
                ],
            )

        self.dialog.open()


    def filter(self, _instance):
        """ Summary
            -------
           Filters the collection with chosen parameters and saves the new
           collection in a list
        """
        field_ids = self.dialog.content_cls.ids

        # retrieves text from the text fields
        title_art       = field_ids.title_input.text
        artist          = field_ids.artist_input.text
        style           = field_ids.style_input.text
        technique       = field_ids.technique_input.text
        medium          = field_ids.medium_input.text
        datation_min    = int(field_ids.datation_min_input.text)
        datation_max    = int(field_ids.datation_max_input.text)
        
        # find toggled down button for mode
        mode_text = ''
        for btn in field_ids.mode_btn.children:
            if btn.state == 'down':
                mode_text = btn.text
                break

        true_mode = 'all'
        if mode_text == 'OR':
            true_mode = 'any'

        displayed_images = self.app.CURRENT_COLLECTION.get_collection()

        # filter with the textinput values
        displayed_images = CollectionUtils.filter(displayed_images,
            mode = true_mode,
            title = title_art,
            artist = artist,
            style = style,
            technique = technique,
            material = medium,
            datation_min = datation_min,
            datation_max = datation_max
        )

        # saves the filtered collection in a list and displays it
        self.app.TOOLBAR.displayed_images = displayed_images
        self.app.GRID.set_display_list(displayed_images)
        self.app.TOOLBAR.selected_images = list()

        # close the popup
        self.dialog.dismiss()


    def dismiss_dialog(self, _instance):
        if self.dialog:
            # close the popup
            self.dialog.dismiss()


    def reset_filter(self, _instance):
        field_ids = self.dialog.content_cls.ids
        
        field_ids.title_input.text = ""
        field_ids.artist_input.text = ""
        field_ids.style_input.text = ""
        field_ids.technique_input.text = ""
        field_ids.medium_input.text = ""
        field_ids.datation_min_input.text = "-5000"
        field_ids.datation_max_input.text = "5000"


    def open_export(self):
        """ Summary
            -------
            Opens the filter window with the current filters
        """

        if len(self.selected_images) == 0:
            self.app.show_error("Please select at least one image")
            return

        if not self.dialog:
            self.dialog = MDDialog(
                title="Export",
                type="custom",
                content_cls=ExportDialogContent(),
                buttons=[
                    MDRaisedButton(
                        text="EXPORT",
                        on_release=self.export
                    ),
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=self.dismiss_dialog
                    ),
                ],
            )

        self.dialog.open()


    def export(self, _instance):
        """
            Call plyer filechooser API to run a filechooser Activity.
        """
        field_ids = self.dialog.content_cls.ids

        # get the file type chosen based on the text in the selected
        # button.
        file_type = ''
        for btn in field_ids.file_toggle.children:
            if btn.state == 'down':
                file_type = btn.text.lower()
                break

        try:
            if file_type == "pptx":
                filechooser.save_file(
                    on_selection=self.handle_selection_pptx,
                    filters=["*.%s" % file_type], # FIXME: crashes on replace existing file...
                    use_extensions=True
                )
            elif file_type == "csv":
                filechooser.save_file(
                    on_selection=self.handle_selection_csv,
                    filters=["*.%s" % file_type], # FIXME: crashes on replace existing file...
                    use_extensions=True
                )
        except Exception:
            message = "An error occurred when selecting save destination"
            Logger.exception(message)
            self.app.show_error(message)



    def handle_selection_pptx(self, selection):
        """
        Callback function for handling the selection response from Activity.
        """
        # 2. generate the powerpoint and save it to the selected path

        # get the input export path
        export_path = str(selection[0])

        Logger.info("Arty: exporting selection to pptx...")
        ConfirmationSnackbar(text="Exporting to PowerPoint...").open()

        try:
            Powerpoint.create_presentation(
                self.selected_images,
                self.app.PROJECT_DIRECTORY,
                export_path
            )
        except Exception as exc:
            Logger.exception(exc)
            self.app.show_error("An error occurred while generating the presentation")
        
        # close dialog
        self.dialog.dismiss()


    def handle_selection_csv(self, selection):
        export_path = str(selection[0])

        ConfirmationSnackbar(text="Exporting to CSV...").open()
        CollectionUtils.export_csv(self.selected_images, export_path)

        # close dialog
        self.dialog.dismiss()
        # with open(export_path, "w") as csv_file:
        #     csv_file.write(csv_data)
