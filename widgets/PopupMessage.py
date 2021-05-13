from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import kivy.properties as kyprops

class PopupMessage(Popup):
    """Summary
        -------
        Error Popup

        Attributes
        ----------
        message: StringProperty
            message to diplay

        Methods
        -------

    """

    Builder.load_file('templates/PopupMessage.kv')
    message = kyprops.StringProperty("")
