from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup

from api.Collection import CollectionUtils

class FilterDropdown(Popup):
    """ Summary
        -------
        Dropdown list for the filter options

        Methods
        -------
        filter_by()
    """

    Builder.load_file('templates/FilterDropdown.kv')

    def select_mode(self):

        self.ids.mode_btn.text = 'all'

        if self.ids.mode_btn.state == 'down':
            self.ids.mode_btn.text = 'any'


    def filter_by(self):
        app = App.get_running_app()

        title = self.ids.title_input.text
        artist = self.ids.artist_input.text
        technique = self.ids.technique_input.text
        mode = self.ids.mode_btn.text

        displayed_images = app.TOOLBAR.displayed_images

        if len(displayed_images) == 0:
            displayed_images = app.CURRENT_COLLECTION.get_collection()

        displayed_images = CollectionUtils.filter(displayed_images, 
                                               mode= mode,
                                               title = title,
                                               artist = artist,
                                               technique = technique)
        
        app.TOOLBAR.displayed_images = displayed_images
        app.GRID.set_display_list(displayed_images)
        app.TOOLBAR.selected_images = list()
    
    def reset_grid(self):
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION.get_collection()

        self.ids.title_input.text = ""
        self.ids.artist_input.text = ""
        self.ids.technique_input.text = ""

        app.GRID.set_display_list(collection)
        # reset CollectionToolbar selection
        self.parent.selected_images = list()
