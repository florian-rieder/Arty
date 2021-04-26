import os

from kivy.lang import Builder
from kivy.app import App
from kivy.logger import Logger
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
    # rebind=True allows refreshing the ui when the property changes
    current_image = ObjectProperty(CollectionImage("shadow32.png"), rebind=True)
    source = StringProperty("")

    Builder.load_file('templates/CollectionPanel.kv')


    def initialize(self, work_dir):
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir


    def set_image(self, collection_image):
        """ Summary
            -------
            Set the image to display in the collection panel and try to
            save the metadata of the previous one.

            Arguments
            ---------
            collection_image: CollectionImage
                the CollectionImage to display and edit
        """
        if not isinstance(collection_image, CollectionImage):
            raise TypeError("collection_image must be of type CollectionImage")

        # try to save when the image is changed. Doesn't work on the
        # first try, because of the default image, but we catch it.
        try:
            self.save()
        except Exception:
            Logger.exception("Arty: Couldn't save %s" % self.current_image.filename)

        self.current_image = collection_image
        self.source = self.get_image_source()


    def get_image_source(self):
        """ Summary
            -------
            Get the absolute path to an image in order to display it

            Returns
            -------
            path: str
                absolute path to the image
        """
        return os.path.join(self.WORK_DIRECTORY, self.current_image.filename)


    def save(self):
        """ Summary
            -------
            Saves the metadata of the current collection image
        """
        # a little bit hard-codey but it's okay
        self.current_image.title                = self.ids.meta_title.text
        self.current_image.artist               = self.ids.meta_artist.text
        self.current_image.technique            = self.ids.meta_technique.text
        self.current_image.year                 = self.ids.meta_year.text
        self.current_image.conservation_site    = self.ids.meta_conservation_site.text
        self.current_image.production_site      = self.ids.meta_production_site.text
        self.current_image.dimensions           = self.ids.meta_dimensions.text
        self.current_image.user_notes           = self.ids.meta_user_notes.text

        app = App.get_running_app()
        app.CURRENT_COLLECTION.update_image(self.current_image)
