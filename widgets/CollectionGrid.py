from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.logger import Logger

from api.Collection import Collection
from widgets.CollectionGridImage import CollectionGridImage

class CollectionGrid(GridLayout):
    """
        Summary
        -------
        Displays the collection in grid format.

        Methods
        -------
        set_collection(collection)
            Updates display of the grid with the images in the
            collection. 
    """
    CURRENT_COLLECTION = None

    Builder.load_file('templates/CollectionGrid.kv')

    def set_collection(self, collection):
        if not isinstance(collection, Collection):
            raise ValueError("collection must by of type Collection")

        # remove children if the collection is not None
        if self.CURRENT_COLLECTION:
            self.clear_widgets()

        # set the collection
        self.CURRENT_COLLECTION = collection

        for collection_image in collection.get_collection():
            absolute_path = collection.get_absolute_path(collection_image)

            try:
                image_widget = CollectionGridImage(
                    source = absolute_path, collection_image=collection_image)

                self.add_widget(image_widget)
            except ValueError:
                Logger.exception(
                    'CollectionGrid: Unable to load <%s>' % collection_image
                )

        Logger.info("Arty: CollectionGrid refreshed.")
