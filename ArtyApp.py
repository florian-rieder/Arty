""" Arty is an image viewer for Art History
"""
import os
import platform

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from widgets.Hotkeys import Hotkeys
from widgets.CollectionGrid import CollectionGrid
from widgets.CollectionPanel import CollectionPanel
from widgets.CollectionToolbar import CollectionToolbar
from widgets.PopupMessage import PopupMessage
from screens.StartScreen import StartScreen
from screens.CollectionScreen import CollectionScreen
from screens.ComparisonScreen import ComparisonScreen
from api.Collection import CollectionManager, Collection


class ArtyApp(App):
    """ Summary
        -------
        The main class of our app
    """
    PROJECT_DIRECTORY = ""
    CURRENT_COLLECTION = None
    SCREENS = dict()
    SCREEN_MANAGER = None
    GRID = None
    PANEL = None

    def build(self):
        Logger.info("Platform: System: %s" % platform.system())
        Logger.info("Platform: Release: %s" % platform.release())

        self.icon = "resources/icon.png"

        # bind methods to kivy events
        Window.bind(on_dropfile=self._on_file_drop)
        Window.bind(on_request_close=self._on_request_close)

        # Create different screens
        screen_manager = ScreenManager()

        start_screen      =     StartScreen(name="Start")
        collection_screen =     CollectionScreen(name='Collection')
        comparison_screen =     ComparisonScreen(name="Compare")

        # add hotkeys manager, we're going to use it only in the
        # collection screen for now
        collection_screen.add_widget(Hotkeys())

        # reference important widgets
        self.GRID       =       collection_screen.ids.grid
        self.PANEL      =       collection_screen.ids.panel
        self.TOOLBAR    =       collection_screen.ids.toolbar
        
        # keep reference to all the screens in the app
        self.SCREENS["START"]      =    start_screen
        self.SCREENS["COLLECTION"] =    collection_screen
        self.SCREENS["COMPARE"]    =    comparison_screen

        # add the screens to display
        screen_manager.add_widget(start_screen)
        screen_manager.add_widget(collection_screen)
        screen_manager.add_widget(comparison_screen)

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

            # initialize CollectionPanel
            self.PANEL.initialize(self.PROJECT_DIRECTORY)
            self.PANEL.set_image(self.CURRENT_COLLECTION.get_collection()[0])

            # initialize ComparisonScreen
            self.SCREENS['COMPARE'].initialize(self.PROJECT_DIRECTORY)
        except FileNotFoundError:
            err_msg = "Collection couldn't be loaded at %s" % self.PROJECT_DIRECTORY
            PopupMessage(message=err_msg).open()
            Logger.exception(err_msg)
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

            Arguments
            ---------
            _window (unused)
                Reference to the window
            file_path : str
                Path to the file that was dragged on the window
        """
        # make it so that one can only drop a file if the current screen
        # is the collection screen
        if not self.SCREEN_MANAGER.current == self.SCREENS["COLLECTION"].name:
            err_msg = "Can only drop files on collection screen."
            PopupMessage(message=err_msg).open()
            Logger.exception(err_msg)
            return

        try:
            # add image to the collection
            self.CURRENT_COLLECTION.add_image(file_path)
            # refresh the CollectionGrid
            self.GRID.set_collection(self.CURRENT_COLLECTION)
        except ValueError as err:
            err_msg = "The file %s couldn't be added to the collection." % file_path
            PopupMessage(message=err_msg).open()
            Logger.exception(err)


    def _on_request_close(self, *_args):
        """ Summary
            -------
            Method that runs when the user requests to close the
            application
        """
        # save the metadata in the CollectionPanel in case there are
        # unregistered changes
        try:
            self.PANEL.save()
        except AttributeError:
            Logger.exception("CollectionPanel couldn't save on exit.")
            # return True prevents the app from closing
            #return True
        
        # save the entire collection to disk.
        CollectionManager.save(self.CURRENT_COLLECTION)

        return False

    def on_pause(self):
        """
            Method called when the app is in pause mode (the user
            has minimized the window or moved it to the background)
            Just to be sure, we'll save the collection at that moment.
        """
        CollectionManager.save(self.CURRENT_COLLECTION)
        return True
