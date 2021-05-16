from kivy.uix.button import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.app import App
import kivy.properties as kyprops
import PIL

from widgets.ZoomablePicture import ZoomablePicture

class ImagePreview(ButtonBehavior, Image):
    source = kyprops.StringProperty("")
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

        modal_size = self._get_modal_size()

        # open a modal view to see the image in full size
        large_view = ModalView(
            size_hint=(None, None),
            size=(modal_size),
            background_color=(0,0,0,0),
            auto_dismiss=True
        )

        large_view.add_widget(ZoomablePicture(
            source=self.source,
            image_width=modal_size[0],
            image_height=modal_size[1]
        ))

        # bind on dismiss callback
        large_view.bind(on_dismiss=self._on_large_view_dismissed)

        # open the modal
        large_view.open()
        self.large_view_open = True


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


    def _get_modal_size(self):
        """ Summary
            -------
            Computes the desired size of the modal, in function of the
            size of the image, and the size of the window

            Returns
            -------
            modal_size : tuple
                bi-dimensional tuple containing the x and y size of the
                modal.
        """
        WINDOW_MIN_MARGIN = 0.95

        # size the modal in function of the image size
        with PIL.Image.open(self.source) as im:
            image_width, image_height = im.size
        
        image_ratio = image_width / image_height
        window_ratio = Window.width / Window.height

        if image_ratio < window_ratio:
            # size by height
            ratio = (Window.height * WINDOW_MIN_MARGIN) / image_height
        else:
            # size by width
            ratio = (Window.width * WINDOW_MIN_MARGIN) / image_width

        modal_size = (image_width * ratio, image_height * ratio)
        
        return modal_size


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
        if instance.children[0].scale > 1:
            # prevent closing the modal
            return True
        else:
            self.large_view_open = False
            return False
