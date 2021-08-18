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
        >>>PopupMessage().show_error("your message here")
    """
    dialog = None

    def show_error(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'Error',
                text = message,
                type = 'alert',
                buttons = [
                    MDRaisedButton(
                        text='OK',
                        on_release=self.dismiss_dialog
                    )
                ],
            )
        self.dialog.open()

    def dismiss_dialog(self, _instance):
        print("HERE")
        print(self.dialog)
        if self.dialog:
            # close the popup
            self.dialog.dismiss()