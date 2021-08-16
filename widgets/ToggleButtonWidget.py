from kivy.app import App

from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRaisedButton

class ToggleButtonWidget(MDRaisedButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = App.get_running_app()
        self.background_down = app.theme_cls.primary_dark
