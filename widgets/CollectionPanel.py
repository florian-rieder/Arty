"""
    Panel for displaying a preview of an image and edit its metadata
"""

import os

from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
import kivy.properties as kyprops

from api.Collection import CollectionImage
from widgets.ImagePreview import ImagePreview
from widgets.MetadataItem import MetadataItem
from widgets.Palette import Palette


class CollectionPanel(BoxLayout):
    """
        Summary
        -------
        Panel for each image in wich you can edit the metadata.

        Attributes
        ----------
        WORK_DIRECTORY : string
            Initialized when a collection is loaded. Path to the
            directory we're working on.
        current_image : CollectionImage
            The CollectionImage currently displayed in the panel. Update
            this property to change the image displayed in the panel.

        Methods
        -------
        initialize(work_dir)
            On first launch of the CollectionScreen, give the
            CollectionPanel the path to the work directory and generate
            all text fields in function of CollectionImage attributes.
        get_image_source()
            Generates the absolute path to an image so it can be
            displayed.
        save()
            Loops through the text fields and saves the data to the
            collection.
    """
    WORK_DIRECTORY = ""
    tabs = dict()
    attributes = list()
    # start with a default collection as to cause no errors
    # rebind=True allows refreshing the ui when the property changes
    current_image = kyprops.ObjectProperty(
        CollectionImage("default"), rebind=True
    )

    Builder.load_file('templates/CollectionPanel.kv')


    def initialize(self, work_dir):
        """ Summary
            -------
            Initializes the panel. Generates text fields in function of
            the attributes of CollectionImages.
        """
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir

        # generate text fields
        container = self.ids.metadata_container

        # clear container
        container.clear_widgets()

        attributes = [
            'artist',
            'title',
            'datation',
            'dimensions',
            'material',
            'technique',
            'production_site',
            'conservation_site',
            'notes',
        ]

        # calculate height of metadataitems so the notes cell will be
        # twice as high as the other fields
        base_hint_y = 1 / (len(attributes) + 1)

        # generate all text fields
        for attribute in attributes:
            item = MetadataItem(size_hint_y = base_hint_y)
            item.field_name = attribute
            # TODO: find a way to write a "nice" attribute name, without
            # bloating the save file
            item.ids.label.text = attribute.replace("_", " ").title()
            item.ids.text_input.text = getattr(self.current_image, attribute)

            if attribute == "notes":
                item.size_hint_y = base_hint_y * 2
                item.ids.text_input.multiline = True

            # add the widget
            container.add_widget(item)
            self.tabs[attribute] = item


    def set_image(self, collection_image):
        """ Summary
            -------
            Interface for opening an image in the CollectionPanel

            Arguments
            ---------
            collection_image : CollectionImage
                The image to display in the CollectionImage

            Raises
            ------
            TypeError
                if the collection_image is of the wrong type
        """
        # try to save when the image is changed. Doesn't work on the
        # first try, because of the default image, but we catch it.
        if not isinstance(collection_image, CollectionImage):
            raise TypeError("collection_image must be of type CollectionImage")

        try:
            self.save()
        except Exception:
            # For some obscure reason, this particular call to the
            # logger makes the MacOSX build crash.

            # Logger.exception(
            #     "Arty: Couldn't save %s" % self.current_image.filename
            # )

            pass

        self.current_image = collection_image


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

        for metadata_item in self.ids.metadata_container.children:
            # read the value from TextInput
            field_value = metadata_item.ids.text_input.text

            # save the value to memory
            setattr(self.current_image, metadata_item.field_name, field_value)

        # update the image in the collection (in RAM).
        app = App.get_running_app()
        app.CURRENT_COLLECTION.update_image(self.current_image)


    def on_current_image(self, _instance, image):
        """ Summary
            -------
            Callback called when the current_image property is updated.
            Updates the values of the text fields.

            Arguments
            ---------
            _instance (unused)
            image : CollectionImage
        """

        image_path = self.get_image_source()

        # update preview image
        self.ids.preview.source = image_path

        # update palette
        self.ids.palette.set_image(image_path)

        # updates text fields values
        for metadata_item in self.ids.metadata_container.children:
            # read the value from memory
            field_value = getattr(image, metadata_item.field_name)

            # display the value in TextInput
            metadata_item.ids.text_input.text = field_value
