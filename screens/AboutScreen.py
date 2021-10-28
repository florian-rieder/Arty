from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen


class AboutScreen(Screen):
    Builder.load_file('templates/AboutScreen.kv')