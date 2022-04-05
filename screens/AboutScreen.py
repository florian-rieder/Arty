from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App


class AboutScreen(Screen):
    Builder.load_file('templates/AboutScreen.kv')

    def on_back_released(self):
        """
            Callback that runs when the user clicks the "Back" button.
        """
        app = App.get_running_app()
        coll_screen = app.SCREENS["START"]
        app.SCREEN_MANAGER.switch_to(coll_screen, direction="right")