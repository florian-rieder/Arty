from pptx import Presentation

from api.collection import CollectionImage

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
    @staticmethod
    def create_presentation(self, images_list):
        """ Summary
            -------
            Creates a presentation with all the CollectionImages in a
            list 
        """
        pass


    @staticmethod
    def to_slide(self, image):
        """ Summary
            -------
            Converts a CollectionImage to a Powerpoint slide
        """
        if not isinstance(image, CollectionImage):
            raise ValueError(
                "The specified image must be of type CollectionImage"
            )
        
        # TODO: Create a slide with an image and its legend
        legend = image.to_reference()

        slide = None

        # return the slide
        return slide

if __name__ == "__main__":
    pass