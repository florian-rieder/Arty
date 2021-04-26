from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty


from api.Collection import CollectionImage


class ComparisonScreen(Screen):

    WORK_DIRECTORY = StringProperty("")
    # start with a default collection as to cause no errors
    # rebinds allows refreshing the ui when the property changes
    current_image = ObjectProperty(CollectionImage("shadow32.png"), rebind=True)
    source = StringProperty("")

    Builder.load_file("templates/ComparisonScreen.kv")

    def build(self):
        pass

    def LoadImage(self, Image, Collection):
        current_image = []
        current_image = Image(source= filename)
        #self.current_image = current_image


        if (current_image == 1):
            raise ValueError ('Please select at least 2 images')

        if (current_image == 2):
           return self.layout_2

        elif (current_image == 3):
            return self.layout_3

        elif (current_image == 4):
            return self.layout_4

        else: 
            raise ValueError ('Too many images were selected')
