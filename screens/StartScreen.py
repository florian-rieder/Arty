from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

from widgets.FileChoose import FileChoose


class StartScreen(Screen):
    Builder.load_file('templates/StartScreen.kv')

    def switch_to_about(self):
        app = App.get_running_app()
        app.SCREEN_MANAGER.switch_to(app.SCREENS["ABOUT"], direction ='left')