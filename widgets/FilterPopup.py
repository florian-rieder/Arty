from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
import kivy.properties as kyprops

from api.Collection import CollectionUtils

class FilterPopup(Popup):
    """ Summary
        -------
        Popup window for the filter options

        Methods
        -------
        select_mode()
            on_state mode Tooglebutton changes the filtering mode
        filter_by()
            on_press filter button, filters the current images on the grid
        save_values()
            on_press filter button, saves the entered values in the filter
        reset_grid()
            on_press reset button, resets to the initial grid
    """

    Builder.load_file('templates/FilterPopup.kv')

    title_art = kyprops.StringProperty('')
    artist = kyprops.StringProperty('')
    technique = kyprops.StringProperty('')

    def select_mode(self):

        self.ids.mode_btn.text = 'all'

        if self.ids.mode_btn.state == 'down':
            self.ids.mode_btn.text = 'any'


    def filter_by(self):
        app = App.get_running_app()

        self.title_art = self.ids.title_input.text
        self.artist = self.ids.artist_input.text
        self.technique = self.ids.technique_input.text
        mode = self.ids.mode_btn.text

        displayed_images = app.TOOLBAR.displayed_images

        if len(displayed_images) == 0:
            displayed_images = app.CURRENT_COLLECTION.get_collection()

        displayed_images = CollectionUtils.filter(displayed_images, 
                                               mode= mode,
                                               title = self.title_art,
                                               artist = self.artist,
                                               technique = self.technique)

        app.TOOLBAR.displayed_images = displayed_images
        app.GRID.set_display_list(displayed_images)
        app.TOOLBAR.selected_images = list()

    def save_values(self):
        app = App.get_running_app()

        self.title_art = self.ids.title_input.text
        self.artist = self.ids.artist_input.text
        self.technique = self.ids.technique_input.text

        app.TOOLBAR.title_filter = self.title_art
        app.TOOLBAR.artist_filter = self.artist
        app.TOOLBAR.technique_filter = self.technique
        
        self.dismiss()
        

    def reset_grid(self):
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION.get_collection()

        self.ids.title_input.text = ""
        self.ids.artist_input.text = ""
        self.ids.technique_input.text = ""

        app.GRID.set_display_list(collection)
        # reset CollectionToolbar selection
        self.parent.selected_images = list()
