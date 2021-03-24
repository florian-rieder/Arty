from glob import glob
from random import randint
from os.path import join, dirname
import os
from kivy.app import App
from kivy.logger import Logger

from widgets.Picture import Picture

PROJECT_DIRECTORY="/Users/frieder/Documents/images"

class PicturesApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        if not os.listdir(PROJECT_DIRECTORY):
            raise(FileNotFoundError)

        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(PROJECT_DIRECTORY, '*')):
            try:
                # load the image
                picture = Picture(source=filename, rotation=randint(-30, 30))
                # add to the main field
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True