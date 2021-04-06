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
from api.Collection import Collection


class ArtyApp(App):
    PROJECT_DIRECTORY = StringProperty("testimages")
    CURRENT_COLLECTION = ObjectProperty(None)
    SCREENS = DictProperty(dict())
    SCREEN_MANAGER = ObjectProperty(None)

    """ The main class of our app
    """
    def build(self):
        # the root is created in pictures.kv
        root = self.root

        Window.bind(on_dropfile=self._on_file_drop)

        # Create different screens
        sm = ScreenManager()

        start_screen = StartScreen(name="Start")
        coll_screen = CollectionScreen(name='Collection')
        settings_screen = SettingsScreen(name='Settings')

        self.SCREENS["COLLECTION"] = coll_screen
        
        sm.add_widget(start_screen)
        sm.add_widget(coll_screen)
        sm.add_widget(settings_screen)



        sm.current = start_screen.name
        self.SCREEN_MANAGER = sm
        return sm
    
    def load_collection(self, path):
        self.PROJECT_DIRECTORY = path

        # load or create collection at specified project directory
        try:
            self.CURRENT_COLLECTION = Collection(self.PROJECT_DIRECTORY)
        except FileNotFoundError:
            Logger.exception(
                "Collection couldn't be loaded at %s" % self.PROJECT_DIRECTORY
            )
            return

        # add all images in the collection to display
        for collection_image in self.CURRENT_COLLECTION.get_collection():
            try:
                self._add_collection_image(collection_image)
            except Exception:
                Logger.exception('Pictures: Unable to load <%s>' % collection_image)

        self.SCREEN_MANAGER.switch_to(self.SCREENS["COLLECTION"], direction="down")

    def _add_collection_image(self, collection_image):
        path = os.path.join(self.PROJECT_DIRECTORY, collection_image.filename)
        # load the image
        picture = Picture(source=path)
        # add to the main field
        self.SCREENS["COLLECTION"].add_widget(picture)


    def _on_file_drop(self, window, file_path):
        """ Summary
            -------
            when the user drops a file on the window, we add it to the
            current collection.
        """
        try:
            # add image to the collection
            collection_image = self.CURRENT_COLLECTION.add_image(file_path)
            # add image to display
            self._add_collection_image(collection_image)
        except ValueError:
            Logger.exception("The file %s couldn't be added to the collection." % file_path)

    def on_pause(self):
        return True
