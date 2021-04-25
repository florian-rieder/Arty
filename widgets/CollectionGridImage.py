from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty, ObjectProperty

class CollectionGridImage(AnchorLayout, ButtonBehavior, Image):
    """
        Summary
        -------
        Displays a clickable an selectable image of the collection.
        
        Attributes
        ----------
        source: StringProperty
            source of the image

        Methods
        -------

    """
    Builder.load_file('templates/CollectionGridImage.kv')

    source = StringProperty(None)
    collection_image = ObjectProperty(None)
        