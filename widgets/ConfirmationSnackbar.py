from kivy.lang import Builder
from kivy.core.window import Window
import kivy.properties as kyprops

from kivymd.uix.snackbar import Snackbar

class ConfirmationSnackbar(Snackbar):
    Builder.load_file('templates/ConfirmationSnackbar.kv')