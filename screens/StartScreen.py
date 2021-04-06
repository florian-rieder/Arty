from kivy.uix.screenmanager import Screen
from kivy.app import App

class StartScreen(Screen):
    def load_collection(self, path):
        app = App.get_running_app()
        app.load_collection(path)