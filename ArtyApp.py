""" Arty is an image viewer for Art History
"""
import os

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import StringProperty

from widgets.Picture import Picture
from widgets.CollectionGrid import CollectionGrid
from screens.CollectionScreen import CollectionScreen
from screens.SettingsScreen import SettingsScreen
from api.Collection import Collection


PROJECT_DIRECTORY="testimages"

class ArtyApp(App):
    global CURRENT_COLLECTION
    CURRENT_COLLECTION=None
    global SCREENS
    SCREENS=dict()

    """ The main class of our app
    """
    def build(self):
        # the root is created in pictures.kv
        #root = self.root

        Window.bind(on_dropfile=self._on_file_drop)

        # Create different screens
        sm = ScreenManager()

        coll_screen = CollectionScreen(name='Collection')
        SCREENS["COLLECTION"] = coll_screen
        settings_screen = SettingsScreen(name='Settings')
        sm.add_widget(coll_screen)
        sm.add_widget(settings_screen)

        # load or create collection at specified project directory
        try:
            self.CURRENT_COLLECTION = Collection("test", PROJECT_DIRECTORY)
        except FileNotFoundError:
            Logger.exception("Collection couldn't be loaded at %s" % PROJECT_DIRECTORY)
            return

        # add all images in the collection to display
        for collection_image in self.CURRENT_COLLECTION.get_collection():
            try:
                self._add_collection_image(collection_image)
            except Exception:
                Logger.exception('Pictures: Unable to load <%s>' % collection_image)

        sm.current = coll_screen.name
        return sm


    def _add_collection_image(self, collection_image):
        path = os.path.join(PROJECT_DIRECTORY, collection_image.filename)
        # load the image
        picture = Picture(source=path)
        # add to the main field
        SCREENS["COLLECTION"].add_widget(picture)


    def _on_file_drop(self, window, file_path):
        """ Summary
            -------
            when the user drops a file on the window, we add it to the
            current collection.
        """
        try:
            collection_image = self.CURRENT_COLLECTION.add_image(file_path)
            self._add_collection_image(collection_image)
        except ValueError:
            Logger.exception("The file %s couldn't be added to the collection." % file_path)


    def on_pause(self):
        return True
