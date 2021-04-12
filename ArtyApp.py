""" Arty is an image viewer for Art History
"""
import os

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import DictProperty, ObjectProperty, StringProperty

from widgets.Picture import Picture
from widgets.CollectionGrid import CollectionGrid
from screens.StartScreen import StartScreen
from screens.CollectionScreen import CollectionScreen
from screens.SettingsScreen import SettingsScreen
from api.Collection import CollectionManager, Collection


class ArtyApp(App):
    """ Summary
        -------
        The main class of our app
    """
    PROJECT_DIRECTORY = StringProperty("testimages")
    CURRENT_COLLECTION = ObjectProperty(None)
    SCREENS = DictProperty(dict())
    SCREEN_MANAGER = ObjectProperty(None)

    def build(self):
        # the root is created in pictures.kv
        #root = self.root

        Window.bind(on_dropfile=self._on_file_drop)

        # Create different screens
        screen_manager = ScreenManager()

        start_screen      =     StartScreen(name="Start")
        collection_screen =     CollectionScreen(name='Collection')
        settings_screen   =     SettingsScreen(name='Settings')

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

        # load or create collection at specified project directory
        try:
            self.CURRENT_COLLECTION = CollectionManager.load(self.PROJECT_DIRECTORY)
        except FileNotFoundError:
            Logger.exception(
                "Collection couldn't be loaded at %s" % self.PROJECT_DIRECTORY
            )
            return

        # add all images in the collection to display
        for collection_image in self.CURRENT_COLLECTION.get_collection():
            try:
                self._add_collection_image(collection_image)
            except ValueError:
                Logger.exception(
                    'Pictures: Unable to load <%s>' % collection_image
                )

        # switch to the collection screen
        self.SCREEN_MANAGER.switch_to(
            self.SCREENS["COLLECTION"], 
            direction="down"
        )


    def _add_collection_image(self, collection_image):
        """ Summary
            -------
            Add a collection image to the current collection and display

            Parameters
            ----------
            collection_image : CollectionImage
                the collection image to add
        """
        path = os.path.join(self.PROJECT_DIRECTORY, collection_image.filename)
        # load the image
        picture = Picture(source=path)
        # add to the main field
        self.SCREENS["COLLECTION"].add_widget(picture)


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
            collection_image = self.CURRENT_COLLECTION.add_image(file_path)
            # add image to display
            self._add_collection_image(collection_image)
        except ValueError:
            Logger.exception("The file %s couldn't be added to the collection." % file_path)

    def on_pause(self):
        return True
