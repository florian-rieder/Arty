from kivy.uix.button import ButtonBehavior
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.app import App
import kivy.properties as kyprops

from widgets.LargeImageView import LargeImageView

class ImagePreview(ButtonBehavior, Image):
    source = kyprops.StringProperty("")
    legend = kyprops.StringProperty("")

    is_hovered = False
    large_view_open = False

    app = None


    def __init__(self, **kwargs):
        super(ImagePreview, self).__init__(**kwargs)
        # bind mouse position updates so we can check when the cursor
        # hovers over the image
        # note: had to do it in the init, otherwise it doesn't work
        self.app = App.get_running_app()
        Window.bind(mouse_pos=self.on_mouse_pos)


    def on_press(self):
        """ Summary
            -------
            Runs when the user clicks on the preview. Opens a modal to
            view the image in a larger format
        """
        # open a modal view to see the image in full size
        large_view = LargeImageView(source=self.source, legend=self.legend)

        # pylint: disable=no-member
        large_view.bind(on_dismiss=self._on_large_view_dismissed)

        # open the modal
        large_view.open()
        self.large_view_open = True
        Window.set_system_cursor("arrow")


    def on_mouse_pos(self, window, pos):
        # if the mouse position is over the image
        if (
            self.collide_point(*pos)
            and not self.large_view_open
            and self.app.SCREEN_MANAGER.current == "Collection"
        ):
            if not self.is_hovered:
                self.is_hovered = True
                Window.set_system_cursor("hand")
        else:
            if self.is_hovered:
                self.is_hovered = False
                Window.set_system_cursor("arrow")


    def _on_large_view_dismissed(self, instance):
        """ Summary
            -------
            Callback to intercept the large view modal on_dismiss and
            prevent closing it if the image is zoomed.
            (Prevents unwanted closing of the image when trying to move
            it and clicking out of the borders of the modal, but not of
            the image, but also prevents closing it using escape...)

            Notes
            -----
            There is no way of differenciating a dismiss from clicking
            outside of the modal, or if escape has been pressed in kivy.
            Workaround is yet to be found.
        """
        # prevent closing the modal if the image is zoomed
        if instance.ids.zoomableimage.scale > 1:
            # prevent closing the modal
            return True
        else:
            self.large_view_open = False
            return False
