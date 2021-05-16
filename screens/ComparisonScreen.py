import os

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App
import kivy.properties as kyprops

from api.Collection import CollectionImage

class ComparisonScreen(Screen):
    """
        Summary
        -------
        Screen to compare up to four images.
        
        Attributes
        ----------
        source: StringProperty
            source of the image

        Methods
        -------
        initialize(work_dir)
            Method called at the initialization of the collection. Lets
            this widget know what the work directory is so we can
            display images without a reference to the entire Collection.
        load_images(image_list)
            Takes a list of CollectionImages and switches the user to
            the comparison screen, where it'll display the images in the
            list in a nice layout.
        on_back_released()
            Callback triggered when the user clicks the "Back" button.
            Switches screens back to the CollectionScreen.

    """

    WORK_DIRECTORY = ""
    source = kyprops.StringProperty("")

    Builder.load_file("templates/ComparisonScreen.kv")


    def initialize(self, work_dir):
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir


    def load_images(self, image_list):
        if not isinstance(image_list, list):
            raise TypeError('image_list must be of type list')
        if not 2 <= len(image_list) <= 4:
            raise ValueError(
                'len of image_list is lower than 2 or higher than 4'
            )
        if not all(isinstance(i, CollectionImage) for i in image_list):
            raise TypeError(
                'objects in image_list must be of type CollectionImage'
            )

        self.ids.layout_container.clear_widgets()

        if len(image_list) == 2:
            layout = Layout2()
            self.ids.layout_container.add_widget(layout)
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
        
        if len(image_list) == 3:
            layout = Layout3()
            self.ids.layout_container.add_widget(layout)
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
            layout.ids.image_3.source = os.path.join(self.WORK_DIRECTORY,image_list[2].filename)

        if len(image_list) == 4:
            layout = Layout4()
            self.ids.layout_container.add_widget(layout)
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
            layout.ids.image_3.source = os.path.join(self.WORK_DIRECTORY,image_list[2].filename)
            layout.ids.image_4.source = os.path.join(self.WORK_DIRECTORY,image_list[3].filename)

    def on_back_released(self):
        """
            Callback that runs when the user clicks the "Back" button.
        """
        app = App.get_running_app()
        coll_screen = app.SCREENS["COLLECTION"]
        app.SCREEN_MANAGER.switch_to(coll_screen, direction="right")

class Layout2(Widget):
    pass

class Layout3(Widget):
    pass

class Layout4(Widget):
    pass