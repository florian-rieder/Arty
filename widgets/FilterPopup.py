from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
import kivy.properties as kyprops

from api.Collection import CollectionUtils

class FilterPopup(Popup):
    """ Summary
        -------
        Popup window for the filter options

        Attributes:
        ----------
        title_art: StringProperty
            string of the title textinput
        artist: StringProperty
            string of the artist textinput
        style: StringProperty
            string of the style textinput
        technique: StringProperty
            string of the technique textinput
        mode: StringProperty
            state of the mode togglebutton
        mode_text: StringProperty
            string value of the mode togllebutton


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

    # set textinputs
    title_art = kyprops.StringProperty('')
    artist = kyprops.StringProperty('')
    style = kyprops.StringProperty('')
    technique = kyprops.StringProperty('')
    mode = kyprops.StringProperty('normal')
    mode_text = kyprops.StringProperty('and')

    def select_mode(self):
        """ Summary
            -------
            Changes the text of the mode togglebutton according to state
        """
        self.ids.mode_btn.text = 'and'

        if self.ids.mode_btn.state == 'down':
            self.ids.mode_btn.text = 'or'

    def filter_by(self):
        """ Summary
            -------
           Filters the collection with chosen parameters and saves the new
           collection in a list
        """
        app = App.get_running_app()

        # retrieves text from the textinput
        self.title_art = self.ids.title_input.text
        self.artist = self.ids.artist_input.text
        self.style = self.ids.style_input.text
        self.technique = self.ids.technique_input.text
        self.mode_text = self.ids.mode_btn.text

        true_mode = 'all'
        if self.mode_text == 'or':
            true_mode = 'any'

        displayed_images = app.CURRENT_COLLECTION.get_collection()

        # filter with the textinput values
        displayed_images = CollectionUtils.filter(displayed_images,
                                               mode= true_mode,
                                               title = self.title_art,
                                               artist = self.artist,
                                               style = self.style,
                                               technique = self.technique)

        # saves the filtered collection in a list and displays it
        app.TOOLBAR.displayed_images = displayed_images
        app.GRID.set_display_list(displayed_images)
        app.TOOLBAR.selected_images = list()

    def save_values(self):
        """ Summary
            -------
            Saves the textinput values and closes the filter window
        """
        app = App.get_running_app()

        # retrives the textinput values
        self.title_art = self.ids.title_input.text
        self.artist = self.ids.artist_input.text
        self.style = self.ids.style_input.text
        self.technique = self.ids.technique_input.text
        self.mode = self.ids.mode_btn.state
        self.mode_text = self.ids.mode_btn.text

        # sets the textinput values in the toolbar class
        app.TOOLBAR.title_filter = self.title_art
        app.TOOLBAR.artist_filter = self.artist
        app.TOOLBAR.style_filter = self.style
        app.TOOLBAR.technique_filter = self.technique
        app.TOOLBAR.mode_filter = self.mode
        app.TOOLBAR.mode_text_filter = self.mode_text

        # closes the filter window
        self.dismiss()

    def reset_grid(self):
        """ Summary
            -------
            Clears the filter and resets the grid to the initial collection
        """
        # get the initial collection
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION.get_collection()

        # clears textinputs
        self.title_art = ''
        self.artist = ''
        self.style = ''
        self.technique = ''
        self.mode = 'normal'

        # display initial collection
        app.GRID.set_display_list(collection)
        # reset CollectionToolbar selection
        self.parent.selected_images = list()
