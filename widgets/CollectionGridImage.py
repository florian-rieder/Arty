from kivy.lang import Builder
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty

from api.Collection import CollectionImage

class CollectionGridImage(AnchorLayout, ButtonBehavior, Image):
    """
        Summary
        -------
        Displays a clickable an selectable image of the collection.
        
        Attributes
        ----------
        source: StringProperty
            source of the image
        collection_image: ObjectProperty(CollectionImage)
            the CollectionImage represented by this widget

        Methods
        -------

    """
    Builder.load_file('templates/CollectionGridImage.kv')

    source = StringProperty(None)
    # the default collection prevents getting errors and warnings before
    # the widget is fully initialized
    collection_image = ObjectProperty(CollectionImage("shadow32.png"))

    def on_press(self):
        """ Summary
            -------
            Displays this image in the CollectionPanel when clicked on
        """
        app = App.get_running_app()
        app.PANEL.set_image(self.collection_image)