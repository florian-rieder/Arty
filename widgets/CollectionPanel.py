import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

from api.Collection import CollectionImage

class CollectionPanel(BoxLayout):
    """
        Summary
        -------
        Panel for each image in wich you can edit the metadata.

        Attributes
        ----------

        Methods
        -------

    """
    WORK_DIRECTORY = StringProperty("")
    # start with a default collection as to cause no errors
    # rebinds allows refreshing the ui when the property changes
    current_image = ObjectProperty(CollectionImage("shadow32.png"), rebind=True)
    source = StringProperty("")

    Builder.load_file('templates/CollectionPanel.kv')

    def build(self):
        self.orientation = "vertical"

    def initialize(self, work_dir):
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir

    def set_image(self, collection_image):
        if not isinstance(collection_image, CollectionImage):
            raise TypeError("collection_image must be of type CollectionImage")

        self.current_image = collection_image
        self.source = self.get_image_source()
    
    def get_image_source(self):
        return os.path.join(self.WORK_DIRECTORY, self.current_image.filename)