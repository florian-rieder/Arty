import os

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget

from api.Collection import CollectionImage

class ComparisonScreen(Screen):

    WORK_DIRECTORY = StringProperty("")
    # start with a default collection as to cause no errors
    # rebinds allows refreshing the ui when the property changes
    source = StringProperty("")

    Builder.load_file("templates/ComparisonScreen.kv")

    def build(self):
        pass

    def initialize(self, work_dir):
        # needed to get the full path to an image
        self.WORK_DIRECTORY = work_dir

    def load_images(self, image_list):
        if not isinstance(image_list, list):
            raise TypeError('')
        if not 2 <= len(image_list) <= 4:
            raise ValueError(len(image_list))
        if not all([isinstance(i, CollectionImage) for i in image_list]):
            raise TypeError('')


        if len(image_list) == 2:
            layout = Layout2()
            self.add_widget(layout)
            layout.get_image_1().source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.get_image_2().source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)



class Layout2(Widget):
    def get_image_1(self):
        return self.ids.image_1
    def get_image_2(self):
        return self.ids.image_2