from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.logger import Logger

from api.Collection import Collection
from widgets.CollectionGridImage import CollectionGridImage
from widgets.PopupMessage import PopupMessage

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
        set_display_list(collection_list)
            Displays a list of CollectionImages in the order of the
            list. set_collection() must have been called prior.
    """
    CURRENT_COLLECTION = None

    Builder.load_file('templates/CollectionGrid.kv')

    def set_collection(self, collection):
        if not isinstance(collection, Collection):
            raise ValueError("collection must by of type Collection")

        # set the collection
        self.CURRENT_COLLECTION = collection

        # Initialize with the collection in its default order
        # (alphabetical order of filenames)
        self.set_display_list(self.CURRENT_COLLECTION.get_collection())

        Logger.info("Arty: CollectionGrid refreshed.")


    def set_display_list(self, collection_list):
        """ Summary
            -------
            Will display a list of CollectionImages in the grid, in the
            order of the list.
            A collection must have been set using the set_collection()
            method.

            Arguments
            ---------
            collection_list : list(CollectionImage)
                A list of CollectionImages to display in the grid.
        """
        # remove children if the collection is not None
        if self.CURRENT_COLLECTION:
            self.clear_widgets()

        for collection_image in collection_list:
            # get absolute path to the image, in order to display it
            absolute_path = self.CURRENT_COLLECTION.get_absolute_path(
                collection_image
            )

            try:
                # create an image widget
                image_widget = CollectionGridImage(
                    source=absolute_path,
                    collection_image=collection_image
                )

                # add it to the grid
                self.add_widget(image_widget)

            except ValueError:
                Logger.exception(
                    'CollectionGrid: Unable to load <%s>' % collection_image
                )
                PopupMessage(
                    message = "Unable to load <%s>" % collection_image).open()
