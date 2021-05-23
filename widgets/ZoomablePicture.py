"""
    Displays an image and allows the user to zoom on it up to ten folds,
    and move it around when it is zoomed.
"""

# pylint: disable=no-name-in-module
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from kivy.uix.scatter import ScatterPlane

class ZoomablePicture(ScatterPlane):
    """ Summary
        -------
        Image which can be zoomed on and translated.

        Attributes
        ----------
        source : str
            Absolute path to the image to display
        image_width, image_height : int
            Dimensions of the image in px

        Methods
        -------
        on_touch_up(touch)
            Callback for handling zooming on scroll event
    """
    is_zoomed = False

    def on_touch_up(self, touch):
        """
            Callback for handling zooming on scroll event
        """
        #pos = self.to_widget(*touch.pos)
        pos = touch.pos

        # override Scatter's `on_touch_up` behavior for mouse scroll
        if self.collide_point(*pos):
            if touch.is_mouse_scrolling:
                if touch.button == 'scrollup':
                    # unzoom
                    if self.scale > 1:
                        mat = Matrix().scale(.9, .9, .9)
                        self.apply_transform(mat, anchor=pos)
                    else:
                        # move the image back to the center of the
                        # screen when it reaches a scale of <= 1
                        self.scale = 1
                        self.center = Window.center

                elif touch.button == 'scrolldown':
                    # zoom
                    if self.scale < 10:
                        mat = Matrix().scale(1.1, 1.1, 1.1)
                        self.apply_transform(mat, anchor=pos)

        # allow translating the image on both axis only when it is
        # zoomed
        if self.scale <= 1 and self.do_translation == (True, True):
            self.do_translation = (False, False)
        elif self.scale > 1 and self.do_translation == (False, False):
            self.do_translation = (True, True)

        # if some other kind of "touch": Fall back on Scatter's behavior
        return super().on_touch_up(touch)
