from kivy.lang import Builder
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
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
        is_hovered: Boolean
            True if the mouse is on the widget
        collection_image: ObjectProperty(CollectionImage)
            the CollectionImage represented by this widget

        Methods
        -------
        on_press():
            displays the panel for the image when pressed
        checkbox_click():
            selects the image if the checkbox is clicked
        on_mouse_pos:
            displays the checkbox if the mouse is on the image

    """
    Builder.load_file('templates/CollectionGridImage.kv')

    source = kyprops.StringProperty("")
    is_hovered = False
    # the default collection prevents getting errors and warnings before
    # the widget is fully initialized, but then, it does throw an other
    # error down the line (which is caught so everything is fine)
    collection_image = kyprops.ObjectProperty(CollectionImage("shadow32.png"))

    def __init__(self, **kwargs):
        super(CollectionGridImage, self).__init__(**kwargs)
        # bind mouse position updates so we can check when the cursor
        # hovers over the image
        # note: had to do it in the init, otherwise it doesn't work
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_press(self):
        """ Summary
            -------
            Displays this image in the CollectionPanel when clicked on
        """
        app = App.get_running_app()
        app.PANEL.set_image(self.collection_image)

    def checkbox_click(self, _instance, is_checked):
        """ Summary
            -------
            Saves the image in a list when it's checkbox is clicked
        """

        app = App.get_running_app()

        if is_checked:
            if self.collection_image not in app.TOOLBAR.selected_images:
                app.TOOLBAR.selected_images.append(self.collection_image)
        else:
            if self.collection_image in app.TOOLBAR.selected_images:
                app.TOOLBAR.selected_images.remove(self.collection_image)
    
    def on_mouse_pos(self, window, pos):
        """ Summary
            -------
            Displays the checkbox when the mouse hovers the image
        """

        empty = 'resources/empty.png'
        blank_checkbox = 'resources/blank-check-box.png'

        # convert window position to local position
        rel_pos = self.to_widget(*pos)

        # if the mouse position is over the image
        if self.collide_point(*rel_pos):
            if not self.is_hovered:
                self.is_hovered = True
                self.ids.select_image.background_checkbox_normal = blank_checkbox
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.ids.select_image.background_checkbox_normal = empty