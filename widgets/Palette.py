from PIL import Image

from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.logger import Logger

class Palette(Widget):
    """ Summary
        -------
        Computes and displays the palette of dominant colors of an image

        Methods
        -------
        set_image(image_path)
            Calculates and displays the palette of an image
    """
    NUM_COLORS = 7
    RESIZE = 100

    current_palette = list()

    def __init__(self, **kwargs):
        super(Palette, self).__init__(**kwargs)
        Window.bind(on_resize=self._on_resize)


    def set_image(self, image_path):
        """ Summary
            -------
            Calculates and displays the palette of an image

            Arguments
            ---------
            image_path : str
                Absolute path to the image of which the palette is
                wanted.
        """
        palette = self.get_colors(image_path)
        # remap RGB values [0-255] -> [0-1]
        kivy_palette = [[v / 255 for v in color] for color in palette]

        self.current_palette = kivy_palette
        self._display_palette()


    def _display_palette(self):
        """ Summary
            -------
            Takes a palette and displays it using the canvas.
        """
        self.canvas.clear()
        rectangle_width = self.width / self.NUM_COLORS

        for idx, color in enumerate(self.current_palette):
            with self.canvas:
                Color(*color)
                Rectangle(
                    pos=(
                        self.pos[0] + (rectangle_width * idx),
                        self.pos[1]
                        ),
                    size=(
                        rectangle_width,
                        self.height
                        )
                    )


    @classmethod
    def get_colors(cls, image_path):
        """ Summary
            -------
            Gets the palette of an image

            Arguments
            ---------
            image_path : str
                Absolute path to the image of which the palette is
                wanted.

            Returns
            -------
            list(tuple):
                A list of tuples containing the RGB values of the color,
                in a range from 0 to 255.


            Adapted from : https://gist.github.com/zollinger/1722663
        """
        # Resize image to speed up processing
        img = Image.open(image_path)
        img = img.copy()
        img.thumbnail((cls.RESIZE, cls.RESIZE))

        # Reduce to palette
        paletted = img.convert(
            'P',
            palette=Image.ADAPTIVE,
            colors=cls.NUM_COLORS
        )

        # Find dominant colors
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        colors = list()
        for i in range(cls.NUM_COLORS):
            try:
                palette_index = color_counts[i][1]
                dominant_color = palette[palette_index*3:palette_index*3+3]
                colors.append(tuple(dominant_color))
            except IndexError:
                Logger.exception(
                    "{image_path} has less than {num_colors} colors."
                    .format(
                        image_path = image_path,
                        num_colors = cls.NUM_COLORS
                    )
                )
                break

        return colors


    def _on_resize(self, *_args):
        # reload the palette (fixes positioning and sizing issue)
        self._display_palette()
