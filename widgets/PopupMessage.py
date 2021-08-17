from kivy import app
from kivy.lang import Builder
from kivy.app import App
import kivy.properties as kyprops
from kivymd.uix import dialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

class PopupMessage():
    """ Summary
        -------
        Error popup

        Attributes
        ----------
        message: StringProperty
            message to diplay

        Examples
        --------
        >>>from widgets.PopupMessage import PopupMessage
        >>>PopupMessage(message="your message here").open()
    """

    Builder.load_file('templates/PopupMessage.kv')
    dialog = None

    def show_error(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'ERROR',
                text = message,
                type = 'alert',
                buttons = [
                    MDRaisedButton(
                        text = 'OK',
                        on_release= self.dismiss_dialog

                    )
                ],
            )
        self.dialog.open()

    def dismiss_dialog(self, _instance):
        if self.dialog:
            # close the popup
            self.dialog.dismiss()