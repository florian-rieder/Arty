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
        is_hovered : bool
            True if the mouse is hovering the picture
        MIN_ZOOM : int
            Minimal zoom factor
        MAX_ZOOM : int
            Maximal zoom factor

        Methods
        -------
        on_touch_up(touch)
            Callback for handling zooming on scroll event
    """
    is_zoomed = False

    MIN_ZOOM = 1
    MAX_ZOOM = 12

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
                    if self.scale > self.MIN_ZOOM:
                        mat = Matrix().scale(.9, .9, .9)
                        self.apply_transform(mat, anchor=pos)
                    else:
                        # move the image back to the center of the
                        # screen when it reaches a scale of <= 1
                        # a little hack because translating the image
                        # while zoomed-in would change the center of the
                        # widget when zooming back out, plus the min zoom
                        # could be < 1 due to fast scrolling
                        self.scale = self.MIN_ZOOM
                        self.center = Window.center

                elif touch.button == 'scrolldown':
                    # zoom
                    if self.scale < self.MAX_ZOOM:
                        mat = Matrix().scale(1.1, 1.1, 1.1)
                        self.apply_transform(mat, anchor=pos)


        # restrict translating the image unless it is zoomed
        if self.scale <= 1 and self.do_translation == (True, True):
            self.do_translation = (False, False)
        elif self.scale > 1 and self.do_translation == (False, False):
            self.do_translation = (True, True)

        # if some other kind of "touch": Fall back on Scatter's behavior
        return super().on_touch_up(touch)
