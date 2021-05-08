import os
import json

from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
import kivy.properties as kyprops

from api.Collection import CollectionImage
from widgets.ImagePreview import ImagePreview
from widgets.TabTextInput import TabTextInput
from widgets.MetadataItem import MetadataItem


class CollectionPanel(BoxLayout):
    """
        Summary
        -------
        Panel for each image in wich you can edit the metadata.

        Attributes
        ----------

        Methods
        -------
        set_image(CollectionImage)

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
            the attributes of CollectionImages, and links them in order
            to switch between them with Tab.
        """
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir

        #               *** generate text fields ***
        container = self.ids.metadata_container

        # get the attributes of a CollectionImage using this json trick
        bogus_image = CollectionImage("")
        self.attributes = list(json.loads(bogus_image.to_json()).keys())

        # the filename is not a field that should be changed
        del self.attributes[self.attributes.index("filename")]
        print(self.attributes)

        # generate all fields
        for attribute in self.attributes:
            item = MetadataItem()
            # find a way to write a "nice" attribute name, without
            # bloating the save file
            item.field_name = attribute
            item.ids.label.text = attribute.replace("_", " ").title()
            print(attribute)
            item.ids.text_input.text = getattr(self.current_image, attribute)

            # add the widget
            container.add_widget(item)
            self.tabs[attribute] = item

        # link fields together so we can navigate with the Tab key
        # this links each field to the next one, and the last one to the
        # first
        for idx, attribute in enumerate(reversed(self.attributes)):
            text_input = self.tabs[attribute].ids.text_input
            text_input.set_next(self.tabs[self.attributes[idx - 1]].ids.text_input)


    def set_image(self, collection_image):
        """ Summary
            -------
            Set the image to display in the collection panel and try to
            save the metadata of the previous one.

            Arguments
            ---------
            collection_image: CollectionImage
                The CollectionImage to display and edit
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
        self.ids.preview.source = self.get_image_source()


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

            # save the value
            setattr(self.current_image, metadata_item.field_name, field_value)

        app = App.get_running_app()
        app.CURRENT_COLLECTION.update_image(self.current_image)


    def on_current_image(self, instance, image):
        """ Summary
            -------
            Callback called when the current_image property is updated.
            Updates the values of the text fields.
        """
        for metadata_item in self.ids.metadata_container.children:
            # read the value
            field_value = getattr(self.current_image, metadata_item.field_name)

            # display the value in TextInput
            metadata_item.ids.text_input.text = field_value
