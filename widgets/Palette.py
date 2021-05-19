from PIL import Image

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

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

        self._display_palette(kivy_palette)


    def _display_palette(self, palette):
        """ Summary
            -------
            Takes a palette and displays it using the canvas.
        """
        self.canvas.clear()
        for idx, color in enumerate(palette):
            with self.canvas:
                Color(*color)
                Rectangle(
                    pos = (
                        self.pos[0] + (self.width / self.NUM_COLORS * idx),
                        self.pos[1]
                        ),
                    size = (
                        self.width / self.NUM_COLORS,
                        self.height
                        )
                    )


    @classmethod
    def get_colors(cls, image_path, resize=150):
        """ Summary
            -------
            Gets the palette of an image

            Arguments
            ---------
            image_path : str
                Absolute path to the image of which the palette is
                wanted.
            resize : int default=150
                dimensions to resize the image to (lower improves
                performance)

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
        img.thumbnail((resize, resize))

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
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index*3:palette_index*3+3]
            colors.append(tuple(dominant_color))

        return colors
