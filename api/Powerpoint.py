import os

import PIL
from pptx import Presentation
from pptx.util import Inches, Emu
from pptx.enum.text import PP_ALIGN

from api.Collection import CollectionImage

class Powerpoint():
    """ Summary
        -------
        High level interface to interact with the python-pptx module in
        the context of this specific app.

        Methods
        -------
        create_presentation(images_list)
            Creates a presentation with all the CollectionImages in a
            list
        to_slide(image)
            Creates a Powerpoint slide from a CollectionImage
    """
    @classmethod
    def create_presentation(cls, images_list, work_dir, output_path):
        """ Summary
            -------
            Creates a presentation with all the CollectionImages in a
            list 
        """
        if not all([isinstance(i, CollectionImage) for i in images_list]):
            raise TypeError("images_list must contain only CollectionImages")
        
        # create presentation
        prs = Presentation()

        for image in images_list:
            img_path = os.path.join(work_dir, image.filename)

            # create slide
            blank_slide_layout = prs.slide_layouts[6]
            slide = prs.slides.add_slide(blank_slide_layout)

            # create image
            # TODO: max size and centered
            image_open = PIL.Image.open(img_path)

            # this does not center the image...
            #left = int((prs.slide_width - image_open.width) / 2)
            left = Inches(-0.5)
            top = Inches(0.5)
            height = Inches(6)
            slide.shapes.add_picture(img_path, left, top, height=height)

            # create textbox
            # TODO: center bottom
            left = Inches(0)
            top = Inches(6.6)
            width = prs.slide_width
            height = Inches(0.5)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            tf.alignment = PP_ALIGN.CENTER # align center, doesn't work either
            tf.text = image.to_reference()

        prs.save(output_path)


if __name__ == "__main__":
    images = [CollectionImage(filename="botticelli-venus.png", artist="Botticelli", title="La Naissance de Vénus", year="1567", conservation_site="Musée du Louvre, Paris")]
    Powerpoint.create_presentation(images, "/Users/frieder/Documents/images", "test.pptx")