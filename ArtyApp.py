""" Arty is an image viewer for Art History
"""
import os
import platform

from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from widgets.Hotkeys import Hotkeys
from widgets.CollectionPanel import CollectionPanel
from widgets.CollectionToolbar import CollectionToolbar

from screens.StartScreen import StartScreen
from screens.CollectionScreen import CollectionScreen
from screens.ComparisonScreen import ComparisonScreen
from screens.AboutScreen import AboutScreen

from api.Collection import CollectionManager


class ArtyApp(MDApp):
    """ Summary
        -------
        The main class of our app

        Methods
        -------
        load_collection(path)
            Load a collection from a path
    """

    # Global variables
    PROJECT_DIRECTORY = ""
    CURRENT_COLLECTION = None

    # Reference to particular UI elements
    SCREENS = dict()
    SCREEN_MANAGER = None
    GRID = None
    PANEL = None
    TOOLBAR = None

    dialog = None


    def build(self):
        Logger.info("Platform: System: %s" % platform.system())
        Logger.info("Platform: Release: %s" % platform.release())

        self.icon = "resources/icon.png"

        # set KivyMD color palettes
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        # bind methods to kivy events
        Window.bind(on_dropfile=self._on_file_drop)
        Window.bind(on_request_close=self._on_request_close)

        # Create different screens
        screen_manager = ScreenManager()

        start_screen      =     StartScreen(name="Start")
        collection_screen =     CollectionScreen(name='Collection')
        comparison_screen =     ComparisonScreen(name="Compare")
        about_screen      =     AboutScreen(name="About")

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
        self.SCREENS["ABOUT"]      =    about_screen

        # add the screens to display
        screen_manager.add_widget(start_screen)
        screen_manager.add_widget(collection_screen)
        screen_manager.add_widget(comparison_screen)
        screen_manager.add_widget(about_screen)

        # select the start screen
        screen_manager.current = start_screen.name

        # keep reference to the ScreenManager
        self.SCREEN_MANAGER = screen_manager

        # select the screen manager as root of the application
        return screen_manager
    

    def load_collection(self, path):
        """ Summary
            -------
            Load a collection from the path to a directory.
            Setup other screens and widgets that depend on the
            collection, and switch to the collection screen.

            Arguments
            ---------
            path : str
                Path to the work directory

        """
        self.PROJECT_DIRECTORY = path

        try:
            # load or create collection at specified project directory
            self.CURRENT_COLLECTION = CollectionManager.load(self.PROJECT_DIRECTORY)

        except FileNotFoundError as exc:
            err_msg = "Folder not found: %s" % self.PROJECT_DIRECTORY
            self.show_error(err_msg)
            Logger.exception(exc)
            Logger.exception(err_msg)
            return

        except Exception as exc:
            err_msg = "Collection couldn't be loaded due to an old or corrupted {meta} file".format(meta=CollectionManager.META_EXTENSION)
            self.show_error(err_msg)
            Logger.exception(exc)
            Logger.exception(err_msg)
            return

        # give the collection to the CollectionGrid, which will in turn
        # display the images on the screen
        self.GRID.set_collection(self.CURRENT_COLLECTION)
        self.TOOLBAR.displayed_images = self.CURRENT_COLLECTION.get_collection()

        # initialize CollectionPanel
        self.PANEL.initialize(self.PROJECT_DIRECTORY)
        self.PANEL.set_image(self.CURRENT_COLLECTION.get_collection()[0])

        # initialize ComparisonScreen
        self.SCREENS['COMPARE'].initialize(self.PROJECT_DIRECTORY)

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
        # clean the path given by the file drop
        file_path = str(file_path.decode('utf-8'))
        if file_path.startswith("b'") and file_path.endswith("'"):
            file_path = file_path[2:-1]

        # load a collection when it is dragged on the app
        # It also works when the app is opened by clicking on an Arty 
        # meta file (but only on MacOS it seems.)
        if file_path.endswith(CollectionManager.META_EXTENSION):
            Logger.info("Loading collection from drop...")
            self.load_collection(os.path.dirname(file_path))
            return
                
        # make it so that one can only drop a file if the current screen
        # is the collection screen
        if not self.SCREEN_MANAGER.current == self.SCREENS["COLLECTION"].name:
            # to localize
            err_msg = "Can only drop files on collection screen."
            self.show_error(err_msg)
            Logger.exception(err_msg)
            return

        try:
            # add image to the collection
            self.CURRENT_COLLECTION.add_image(file_path)
            # refresh the CollectionGrid
            self.GRID.set_collection(self.CURRENT_COLLECTION)

        except ValueError as err:
            err_msg = "The file %s couldn't be added to the collection." % file_path
            self.show_error(err_msg)
            Logger.exception(err)


    def _on_request_close(self, *_args):
        """ Summary
            -------
            Method that runs when the user requests to close the
            application.
            We try to save the collection before the app exits.
        """
        # save the metadata in the CollectionPanel in case there are
        # unregistered changes
        if self.CURRENT_COLLECTION:
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
            has minimized the window or moved it to the background).
            Probably only works on mobiles but just in case....
            Just to be sure, we'll save the collection at that moment.
        """
        Logger.info("Arty is paused.")
        CollectionManager.save(self.CURRENT_COLLECTION)

        return True


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
        if self.dialog:
            # close the popup
            self.dialog.dismiss()
            self.dialog = None
