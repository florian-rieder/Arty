from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

from widgets.CollectionImageList import CollectionImageList

class CollectionScreen(Screen):
    Builder.load_file("templates/CollectionScreen.kv")