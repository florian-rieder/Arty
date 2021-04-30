import PIL
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.core.window import Window

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

        # size the modal in function of the image size
        with PIL.Image.open(self.source) as im:
            image_width, image_height = im.size
        
        image_ratio = image_width / image_height
        window_ratio = Window.width / Window.height

        if image_height > image_width or image_ratio < window_ratio:
            # size by height
            height_ratio = (Window.height * self.WINDOW_MIN_MARGIN) / image_height
            modal_size = (image_width * height_ratio, image_height * height_ratio)
        else:
            # size by width
            width_ratio = (Window.width * self.WINDOW_MIN_MARGIN) / image_width
            modal_size = (image_width * width_ratio, image_height * width_ratio)

        # open a modal view to see the image in full size
        modal = ModalView(size_hint=(None, None), size=modal_size)

        modal.add_widget(Image(source=self.source, allow_stretch=True))

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
