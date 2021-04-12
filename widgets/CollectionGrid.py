from os.path import join
from glob import glob

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from api.Collection import Collection
from widgets.CollectionGridImage import CollectionGridImage

class CollectionGrid(GridLayout):
    """
        Summary
        -------
        Displays the collection in grid format.
        
        Attributes
        ----------

        Methods
        -------

    """
    def __init__(self, **kwargs):
        super(CollectionGrid, self).__init__(**kwargs)

        # not the right way to do it, I'll come back to this
        # - Florian
        self.PROJECT_DIRECTORY = App.get_running_app().PROJECT_DIRECTORY
        self.CURRENT_COLLECTION = Collection(self.PROJECT_DIRECTORY)
        self.collection = self.CURRENT_COLLECTION.get_collection()

        
        for collection_image in self.collection:
            for filename in glob(join(self.PROJECT_DIRECTORY, collection_image.filename)):
                print(collection_image.filename)
                self.image_button = CollectionGridImage(source = filename)
                print(self.image_button)
                self.add_widget(self.image_button)

