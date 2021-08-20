from kivy.lang import Builder

from kivymd.uix.snackbar import Snackbar

class ConfirmationSnackbar(Snackbar):
    Builder.load_file('templates/ConfirmationSnackbar.kv')