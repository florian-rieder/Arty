"""
    Hotkeys manager (Ctrl+S saves the collection)
"""

import platform

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window, Keyboard
from kivy.logger import Logger

from api.Collection import CollectionManager
from widgets.ConfirmationSnackbar import ConfirmationSnackbar


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

        self.app = App.get_running_app()
        self.system_name = platform.system()


    def _keyboard_released(self, _keyboard=None, keycode=(0, "")):
        """
            Reset key combination when the Ctrl/Cmd key is released
        """

        if keycode[1] in ('super', 'lctrl'):
            self.super = []


    def _keyboard_on_key_down(self, _window, keycode, _text, _super):
        """ Summary
            -------
            Handle keystrokes:
            Ctrl/Cmd + S : save the current collection
            Ctrl/Cmd + A : select all images

            Arguments
            ---------
            keycode : tuple
                Tuple (keycode : int, keycode : str) indicating the key
                pressed.
        """

        if keycode[1] == 'escape':
            self.escape()


        ###
        # MacOSX hotkeys definition
        if self.system_name == "Darwin":
            # "super" is the keycode for the Command key

            # Cmd + S -> save collection
            if "super" in self.super and keycode[1] == 's':
                return self.save()

            # Cmd + A -> select all images
            elif "super" in self.super and keycode[1] == 'a':
                return self.select_all()

            # Cmd + E -> export selection to pptx
            elif "super" in self.super and keycode[1] == 'e':
                return self.export()

            # remember if cmd is pressed
            elif "super" not in self.super and keycode[1] in ("super"):
                self.super.append(keycode[1])
                return False

            else:
                Logger.info("key {} pressed.".format(keycode))
                return False
        # End MacOSX hotkeys definition
        ###


        ###
        # Windows hotkeys definition
        elif self.system_name == "Windows":
            # Ctrl + S -> save collection
            if 'lctrl' in self.super and keycode[1] == 's':
                return self.save()

            # Ctrl + A -> select all images
            elif 'lctrl' in self.super and keycode[1] == 'a':
                return self.select_all()

            # Ctrl + E -> export selection
            elif 'lctrl' in self.super and keycode[1] == 'e':
                return self.export()

            # remember if lctrl is pressed
            elif 'lctrl' not in self.super and keycode[1] in ("lctrl"):
                self.super.append(keycode[1])
                return False

            else:
                #Logger.info("key {} pressed.".format(keycode))
                return False
        # End Windows hotkeys definition
        ###


    def save(self):
        """ Summary
            -------
            Save the collection

            Returns
            -------
            bool
                Always False. It has got something to do with the kivy
                _on_keyboard_key_down callback.
        """
        collection = self.app.CURRENT_COLLECTION

        # check that there is a collection to save
        if not collection:
            return False

        # save the collection
        self.app.PANEL.save()
        CollectionManager.save(collection)
        ConfirmationSnackbar().open()

        return False


    def select_all(self):
        """ Summary
            -------
            Selects all images via the toolbar

            Returns
            -------
            bool
                Always False. It has got something to do with the kivy
                _on_keyboard_key_down callback.
        """
        # check that we are in the collection screen
        if self.app.SCREEN_MANAGER.current != "Collection":
            return False

        # select all images via the toolbar
        self.app.TOOLBAR.select_all()

        return False


    def export(self):
        """ Summary
            -------
            Save the collection

            Returns
            -------
            bool
                Always False. It has got something to do with the kivy
                _on_keyboard_key_down callback.
        """
        # check that we are in the collection screen
        if self.app.SCREEN_MANAGER.current != "Collection":
            return False

        # export selection via the toolbar
        self.app.TOOLBAR.export()

        return False


    def escape(self):
        """ Summary
            -------
            Escape behavior.

            On Comparison Screen:
                return to collection
        """

        # Comparison Screen
        if self.app.SCREEN_MANAGER.current == "Compare":
            # switch to collection screen
            self.app.SCREEN_MANAGER.switch_to(
                self.app.SCREENS["COLLECTION"],
                direction='right')

        return False
