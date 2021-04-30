import PIL
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.core.window import Window

from widgets.ZoomablePicture import ZoomablePicture

class ImagePreview(ButtonBehavior, Image):
    source = StringProperty("")
    is_hovered = False
    WINDOW_MIN_MARGIN = 0.95

    def __init__(self, **kwargs):
        super(ImagePreview, self).__init__(**kwargs)
        # bind mouse position updates so we can check when the cursor
        # hovers over the image
        # note: had to do it in the init, otherwise it doesn't work
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_press(self):
        """ Summary
            -------
            runs when the user clicks on the preview. Opens a modal to
            view the image in a larger format

            TODO: Figure out how to zoom in the image
        """

        modal_size = self._get_modal_size()

        # open a modal view to see the image in full size
        modal = ModalView(size_hint=(None, None), size=(modal_size), background_color=(0,0,0,0))

        modal.add_widget(ZoomablePicture(source=self.source, image_width=modal_size[0], image_height=modal_size[1]))

        # open the modal
        modal.open()


    def on_mouse_pos(self, window, pos):
        # TODO: figure out how to make it work also on the first element
        # displayed... weird
        # if the mouse position is over the image
        if self.collide_point(*pos):
            if not self.is_hovered:
                self.is_hovered = True
                Window.set_system_cursor("hand")
        else:
            if self.is_hovered:
                self.is_hovered = False
                Window.set_system_cursor("arrow")

    def _get_modal_size(self):
        # size the modal in function of the image size
        with PIL.Image.open(self.source) as im:
            image_width, image_height = im.size
        
        image_ratio = image_width / image_height
        window_ratio = Window.width / Window.height

        if image_height > image_width or image_ratio < window_ratio:
            # size by height
            ratio = (Window.height * self.WINDOW_MIN_MARGIN) / image_height
            modal_size = (image_width * ratio, image_height * ratio)
        else:
            # size by width
            ratio = (Window.width * self.WINDOW_MIN_MARGIN) / image_width
            modal_size = (image_width * ratio, image_height * ratio)
        
        return modal_size