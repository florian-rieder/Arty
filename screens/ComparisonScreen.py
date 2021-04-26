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
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
        
        if len(image_list) == 3:
            layout = Layout3()
            self.add_widget(layout)
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
            layout.ids.image_3.source = os.path.join(self.WORK_DIRECTORY,image_list[2].filename)

        if len(image_list) == 4:
            layout = Layout4()
            self.add_widget(layout)
            layout.ids.image_1.source = os.path.join(self.WORK_DIRECTORY,image_list[0].filename)
            layout.ids.image_2.source = os.path.join(self.WORK_DIRECTORY,image_list[1].filename)
            layout.ids.image_3.source = os.path.join(self.WORK_DIRECTORY,image_list[2].filename)
            layout.ids.image_4.source = os.path.join(self.WORK_DIRECTORY,image_list[3].filename)


class Layout2(Widget):
    pass


class Layout3(Widget):
    pass

class Layout4(Widget):
    pass