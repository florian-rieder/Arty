from PIL import Image

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
import kivy.properties as kyprops

from api.Geometry import Geometry

from widgets.ZoomablePicture import ZoomablePicture


class LargeImageView(ModalView):
    source = kyprops.StringProperty("")
    legend = kyprops.StringProperty("")

    WINDOW_MARGIN = 75 #px


    Builder.load_file('templates/LargeImageView.kv')


    def __init__(self, **kwargs):
        super(LargeImageView, self).__init__(**kwargs)
        Window.bind(on_resize=self._on_resize)

        # get image size
        with Image.open(self.source) as im:
            image_size= im.size

        modal_size = Geometry.fit_to_container(image_size, (Window.width, Window.height), padding=self.WINDOW_MARGIN)
        self.size = modal_size

        img = self.ids.realimage
        img.width = modal_size[0]
        img.height = modal_size[1]


    def _on_resize(self, window, *_args):

        with Image.open(self.source) as im:
            image_size = im.size

        new_size = Geometry.fit_to_container(image_size, (window.width, window.height), padding=self.WINDOW_MARGIN)
        self.size = new_size
        # resize the image inside the ZoomableImage widget (which is a
        # ScatterPlane !)
        self.ids.zoomableimage.children[0].size = new_size
