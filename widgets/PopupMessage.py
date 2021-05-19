from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import kivy.properties as kyprops

class PopupMessage(Popup):
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
    message = kyprops.StringProperty("")
