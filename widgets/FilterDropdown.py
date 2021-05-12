from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import kivy.properties as kyprops

from api.Collection import CollectionUtils

class FilterDropdown(DropDown):
    """ Summary
        -------
        Dropdown list for the filter options

        Methods
        -------
        filter_by()
    """

    Builder.load_file('templates/FilterDropdown.kv')

    def filter_by(self):
        app = App.get_running_app()

        title = self.ids.title_input.text
        artist = self.ids.artist_input.text
        technique = self.ids.technique_input.text

        # TODO: Changer pour obtenir la liste d'images depuis
        # CollectionToolbar
        images_list = app.CURRENT_COLLECTION.get_collection()

        filtered_coll = CollectionUtils.filter(images_list, 
                                               mode='all',
                                               title = title,
                                               artist = artist,
                                               technique = technique)
        
        app.GRID.set_display_list(filtered_coll)