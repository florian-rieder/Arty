# external imports
from os.path import join
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager
import os

# internal imports
from widgets.Picture import Picture
from screens.CollectionScreen import CollectionScreen
from screens.SettingsScreen import SettingsScreen
from collection.Collection import Collection

PROJECT_DIRECTORY="/Users/frieder/Documents/images"

class ArtyApp(App):
    """ The main class of our app
    """
    def build(self):
        # the root is created in pictures.kv
        root = self.root

        # Create different screens
        sm = ScreenManager()

        coll_screen = CollectionScreen(name='Collection')
        settings_screen = SettingsScreen(name='Settings')
        sm.add_widget(coll_screen)
        sm.add_widget(settings_screen)

        # load or create collection at specified project directory
        try:
            coll = Collection("test", PROJECT_DIRECTORY)
        except FileNotFoundError:
            Logger.exception("Collection couldn't be loaded at %s" % PROJECT_DIRECTORY)
            return

        # add all images in the collection to display
        for collection_image in coll.get_collection():
            try:
                path = join(PROJECT_DIRECTORY, collection_image.filename)
                # load the image
                picture = Picture(source=path)
                # add to the main field
                coll_screen.add_widget(picture)
            except Exception:
                Logger.exception('Pictures: Unable to load <%s>' % collection_image)

        sm.current = coll_screen.name
        return sm


    def on_pause(self):
        return True
