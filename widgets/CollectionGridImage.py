from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty

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
    source = StringProperty(None)
