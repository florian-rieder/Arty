from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.lang import Builder


from api.Collection import CollectionImage
CollectionImage("/Users/carolinerohrbach/Desktop/Planche_contact.jpg")

class ComparisonScreen(Screen):
    
    Builder.load_file("templates/ComparisonScreen.kv")

    def build(self):
        pass

class LoadImage(Image):
    pass