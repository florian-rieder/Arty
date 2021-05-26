from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder

class CollectionScreen(Screen):
    Builder.load_file("templates/CollectionScreen.kv")