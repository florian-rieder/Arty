"""
    Hotkeys manager (Ctrl+S saves the collection)
"""

import platform

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window, Keyboard
from kivy.logger import Logger

from api.Collection import CollectionManager


class Hotkeys(FloatLayout):
    """ Summary
        -------
        Invisible widget which allows for catching keyboard hotkeys.
        Adapted from:
        https://stackoverflow.com/questions/40551774/hotkeys-in-kivy-desktop
    """
    def __init__(self, **kwargs):
        super(Hotkeys, self).__init__(**kwargs)
        self.super = []

        keyboard = Window.request_keyboard(self._keyboard_released, self)
        keyboard.bind(on_key_down=self._keyboard_on_key_down, on_key_up=self._keyboard_released)


    def _keyboard_released(self, *args):
        """
            Reset key combination when the keyboard is released
        """
        self.super = []


    def _keyboard_on_key_down(self, window, keycode, text, super):
        """
            Handle keystrokes (Cmd+S, Ctrl+S)
        """
        app = App.get_running_app()
        collection = app.CURRENT_COLLECTION

        # MacOSX hotkeys definition
        if platform.system() == "Darwin":
            # "super" is the keycode for the Command key
            if "super" in self.super and keycode[1] == 's':
                # Cmd + S -> save collection

                # save the contents of the panel, in case there are
                # unregistered modifications
                app.PANEL.save()
                CollectionManager.save(collection)

                self.super = []
                return False
            elif "super" not in self.super and keycode[1] in ["super"]:
                self.super.append(keycode[1])
                return False
            else:
                #Logger.info("key {} pressed.".format(keycode))
                return False

        # Windows hotkeys definition
        if platform.system() == "Windows":
            if 'lctrl' in self.super and keycode[1] == 's':
                # Ctrl + S -> save collection

                app.PANEL.save()
                CollectionManager.save(collection)

                self.super = []
                return False
            elif 'lctrl' not in self.super and keycode[1] in ["lctrl"]:
                self.super.append(keycode[1])
                return False
            else:
                #Logger.info("key {} pressed.".format(keycode))
                return False
