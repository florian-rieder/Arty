from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen

from widgets.FileChoose import FileChoose


class StartScreen(Screen):
    Builder.load_file('templates/StartScreen.kv')