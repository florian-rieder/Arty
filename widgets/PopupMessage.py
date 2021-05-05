from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty

class PopupMessage(FloatLayout):
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
    message = StringProperty("")

    
