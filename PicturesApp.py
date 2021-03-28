from glob import glob
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
import os

from widgets.Picture import Picture
from Collection import Collection

PROJECT_DIRECTORY="/Users/frieder/Documents/images"

class PicturesApp(App):

    def build(self):
        print("BUILD")
        # the root is created in pictures.kv
        root = self.root

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
                root.add_widget(picture)
            except Exception:
                Logger.exception('Pictures: Unable to load <%s>' % collection_image)

    def on_pause(self):
        return True