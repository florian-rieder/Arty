""" Arty is an image viewer for Art History
"""
import os

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import DictProperty, ObjectProperty, StringProperty

from widgets.CollectionGrid import CollectionGrid
from widgets.CollectionPanel import CollectionPanel
from widgets.CollectionToolbar import CollectionToolbar
from screens.StartScreen import StartScreen
from screens.CollectionScreen import CollectionScreen
from screens.SettingsScreen import SettingsScreen
from api.Collection import CollectionManager, Collection


class ArtyApp(App):
    """ Summary
        -------
        The main class of our app
    """
    PROJECT_DIRECTORY = StringProperty("")
    CURRENT_COLLECTION = ObjectProperty(None)
    SCREENS = DictProperty(dict())
    SCREEN_MANAGER = ObjectProperty(None)
    GRID = ObjectProperty(None)
    PANEL = ObjectProperty(None)

    def build(self):
        self.icon = "resources/icon.png"

        # bind methods to kivy events
        Window.bind(on_dropfile=self._on_file_drop)
        Window.bind(on_request_close=self._on_request_close)

        # Create different screens
        screen_manager = ScreenManager()

        start_screen      =     StartScreen(name="Start")
        collection_screen =     CollectionScreen(name='Collection')
        settings_screen   =     SettingsScreen(name='Settings')

        # reference grid
        self.GRID = collection_screen.ids.grid
        self.PANEL = collection_screen.ids.panel

        # keep reference to all the screens in the app
        self.SCREENS["START"]      =    start_screen
        self.SCREENS["COLLECTION"] =    collection_screen
        self.SCREENS["SETTINGS"]   =    settings_screen
        
        # add the screens to display
        screen_manager.add_widget(start_screen)
        screen_manager.add_widget(collection_screen)
        screen_manager.add_widget(settings_screen)

        # select the start screen
        screen_manager.current = start_screen.name

        # keep reference to the ScreenManager
        self.SCREEN_MANAGER = screen_manager

        return screen_manager
    

    def load_collection(self, path):
        """ Summary
            -------
            Load a collection from the path to a directory.
        """
        self.PROJECT_DIRECTORY = path

        try:
            # load or create collection at specified project directory
            self.CURRENT_COLLECTION = CollectionManager.load(self.PROJECT_DIRECTORY)

            # give the collection to the CollectionGrid, which will in turn
            # display the images on the screen
            self.GRID.set_collection(self.CURRENT_COLLECTION)

            # Initialize CollectionPanel
            self.PANEL.initialize(self.CURRENT_COLLECTION.work_directory)
            self.PANEL.set_image(self.CURRENT_COLLECTION.get_collection()[0])
        except FileNotFoundError:
            Logger.exception(
                "Collection couldn't be loaded at %s" % self.PROJECT_DIRECTORY
            )
            return

        # switch to the collection screen
        self.SCREEN_MANAGER.switch_to(
            self.SCREENS["COLLECTION"], 
            direction="down"
        )


    def _on_file_drop(self, _window, file_path):
        """ Summary
            -------
            When the user drops a file on the window, we add it to the
            current collection.
        """
        # make it so that one can only drop a file if the current screen
        # is the collection screen
        if not self.SCREEN_MANAGER.current == self.SCREENS["COLLECTION"].name:
            Logger.exception("Can only drop files on collection screen.")
            return

        try:
            # add image to the collection
            self.CURRENT_COLLECTION.add_image(file_path)
            # refresh the CollectionGrid
            self.GRID.set_collection(self.CURRENT_COLLECTION)
        except ValueError:
            Logger.exception("The file %s couldn't be added to the collection." % file_path)


    def _on_request_close(self, *_args):
        """ Summary
            -------
            Method that runs when the user requests to close the
            application
        """
        # save the metadata in the CollectionPanel, in turn saves the
        # entire collection
        try:
            self.PANEL.save()
        except AttributeError:
            Logger.exception("CollectionPanel couldn't save on exit.")

    def on_pause(self):
        return True
