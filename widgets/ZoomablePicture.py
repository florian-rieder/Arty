from kivy.uix.scatter import ScatterPlane
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.graphics.transformation import Matrix

class ZoomablePicture(ScatterPlane):
    source = StringProperty("")
    image_width = NumericProperty(0)
    image_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ZoomablePicture, self).__init__(**kwargs)

        self.do_rotation = False
        self.do_translation = (False, False)

        # setup image
        image = Image(
            source=self.source,
            height=self.image_height,
            width=self.image_width,
            allow_stretch=True
        )
        self.add_widget(image)


    def on_touch_up(self, touch):
        # Override Scatter's `on_touch_up` behavior for mouse scroll
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    # unzoom
                    if self.scale > 1:
                        mat = Matrix().scale(.9, .9, .9)
                        self.apply_transform(mat, anchor=touch.pos)
                    else:
                        self.center = Window.center
                elif touch.button == 'scrolldown':
                    # zoom
                    if self.scale < 10:
                        mat = Matrix().scale(1.1, 1.1, 1.1)
                        self.apply_transform(mat, anchor=touch.pos)

        if self.scale <= 1 and self.do_translation == (True, True):
            self.do_translation = (False, False)
        elif self.scale > 1 and self.do_translation == (False, False):
            self.do_translation = (True, True)

        # If some other kind of "touch": Fall back on Scatter's behavior
        return super().on_touch_up(touch)
