from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.core.window import Window

class ImagePreview(ButtonBehavior, Image):
    source = StringProperty("")
    # TODO: change cursor when hovering on the preview
    # using Window.set_system_cursor
    is_hovered = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # bind mouse position updates so we can verify when the cursor
        # hovers over the image
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_press(self):
        """ Summary
            -------
            runs when the user clicks on the preview. Opens a modal to
            view the image in a larger format
        """

        # open a modal view to see the image in full size
        modal = ModalView()
        # TODO: Figure out how to make the image the largest they can be
        # and how to make it so that the modal closes when 
        # TODO: Figure out how to dismiss the modal by clicking on the
        # sides
        # TODO: Figure out how to zoom in the image
        modal.add_widget(Image(source=self.source))

        # open the modal
        modal.open()


    def on_mouse_pos(self, window, pos):
        # for now it doesn't work
        # if the mouse position is over the image
        if self.collide_point(*pos):
            if not self.is_hovered:
                print("hand")
                self.is_hovered = True
                Window.set_system_cursor("ibeam")
        else:
            if self.is_hovered:
                print("arrow")
                self.is_hovered = False
                Window.set_system_cursor("arrow")
