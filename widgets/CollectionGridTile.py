from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.behaviors.button import ButtonBehavior
import kivy.properties as kyprops

from kivymd.uix.imagelist import SmartTileWithLabel


EMPTY = 'resources/empty.png'
BLANK_CHECKBOX = 'resources/blank-check-box.png'


class CollectionGridTile(SmartTileWithLabel, ButtonBehavior):
    """
        Summary
        -------
        Displays a clickable and selectable image of the collection.

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

    source = kyprops.StringProperty(None)
    collection_image = kyprops.ObjectProperty(None)
    is_hovered = False

    Builder.load_file("templates/CollectionGridTile.kv")


    def __init__(self, **kwargs):
        super(CollectionGridTile, self).__init__(**kwargs)
        # bind mouse position updates so we can check when the cursor
        # hovers over the image
        # note: had to do it in the init, otherwise it doesn't work
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.text = self.collection_image.to_legend(style_name="SIMPLE")


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
            Saves the image in a list when its checkbox is clicked on

            Arguments
            ---------
            _instance: (unused)
                reference to the current instance
            is_checked: bool
                states if the checkbox is checked
        """

        app = App.get_running_app()

        # appends the image to the selection
        if is_checked:
            if self.collection_image not in app.TOOLBAR.selected_images:
                app.TOOLBAR.selected_images.append(self.collection_image)
        # removes the image from the selection
        else:
            if self.collection_image in app.TOOLBAR.selected_images:
                app.TOOLBAR.selected_images.remove(self.collection_image)


    def on_mouse_pos(self, _window, pos):
        """ Summary
            -------
            Displays the checkbox when the mouse hovers the image

            Arguments
            ---------
            _window (unused)
                reference the app window
            pos: tuple
                position of the cursor
        """

        # convert window position to local position
        rel_pos = self.to_widget(*pos)

        # if the mouse position is over the image, make checkbox visible
        if self.collide_point(*rel_pos):
            if not self.is_hovered:
                self.is_hovered = True
                self.ids.select_image.background_checkbox_normal = BLANK_CHECKBOX
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.ids.select_image.background_checkbox_normal = EMPTY

    def set_collection_image(self, collection_image):
        self.collection_image = collection_image
        self.text = collection_image.to_legend(style_name="SIMPLE")
        print("Collection Image Updated", collection_image)
