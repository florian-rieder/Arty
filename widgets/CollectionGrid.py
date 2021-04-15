from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

from api.Collection import Collection
from widgets.CollectionGridImage import CollectionGridImage

class CollectionGrid(GridLayout):
    """
        Summary
        -------
        Displays the collection in grid format.

        Methods
        -------
        add_image(collection_image, collection)
            Adds a CollectionImage to the grid display
    """

    Builder.load_file('templates/CollectionGrid.kv')

    def add_image(self, collection_image, collection):
        self.image_button = CollectionGridImage(source = collection.get_absolute_path(collection_image))
        self.add_widget(self.image_button)
    

