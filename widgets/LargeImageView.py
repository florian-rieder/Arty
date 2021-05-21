from PIL import Image

from kivy.uix.modalview import ModalView
from kivy.core.window import Window
import kivy.properties as kyprops

from widgets.ZoomablePicture import ZoomablePicture


class LargeImageView(ModalView):
    source = kyprops.StringProperty("")
    WINDOW_MARGIN = 75 #px

    def __init__(self, **kwargs):
        super(LargeImageView, self).__init__(**kwargs)
        Window.bind(on_resize=self._on_resize)

        # ModalView parameters
        self.size_hint=(None, None)
        self.background_color=(0,0,0,0)
        self.auto_dismiss=True

        # size the modal in function of the window size
        modal_size = self._get_size(Window.width, Window.height)
        self.size = modal_size

        # populate the view with the image
        self.add_widget(
            ZoomablePicture(
                source=self.source,
                image_width=modal_size[0],
                image_height=modal_size[1]
            )
        )


    def _get_size(self, window_width, window_height):
        """ Summary
            -------
            Computes the desired size of the modal, in function of the
            size of the image and the size of the window

            Returns
            -------
            modal_size : tuple
                bi-dimensional tuple containing the x and y size of the
                modal.
            window_width : int
            window_height : int
        """

        # size the modal in function of the image size
        with Image.open(self.source) as im:
            image_width, image_height = im.size
        
        image_ratio = image_width / image_height
        window_ratio = window_width / window_height

        if image_ratio < window_ratio:
            # size by height
            height = window_height - self.WINDOW_MARGIN
            width = height * image_ratio
        else:
            # size by width
            width = window_width - self.WINDOW_MARGIN
            height = width / image_ratio

        modal_size = (width, height)
        
        return modal_size


    def _on_resize(self, window, *_args):
        new_size = self._get_size(window.width, window.height)
        self.size = new_size
        # resize the image inside the ZoomableImage widget (which is a
        # ScatterPlane !)
        self.children[0].children[0].size = new_size
