from kivy.lang import Builder
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import kivy.properties as kyprops

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

    source = kyprops.StringProperty("")
    # the default collection prevents getting errors and warnings before
    # the widget is fully initialized, but then, it does throw an other
    # error down the line (which is caught so everything is fine)
    collection_image = kyprops.ObjectProperty(CollectionImage("shadow32.png"))

    def on_press(self):
        """ Summary
            -------
            Displays this image in the CollectionPanel when clicked on
        """
        app = App.get_running_app()
        app.PANEL.set_image(self.collection_image)

    def checkbox_click(self, _instance, is_checked):

        app = App.get_running_app()

        if is_checked:
            app.TOOLBAR.selected_images.append(self.collection_image)
        else:
            app.TOOLBAR.selected_images.remove(self.collection_image)