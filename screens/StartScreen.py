from pathlib import Path

from kivy.uix.screenmanager import Screen
from kivy.app import App

class StartScreen(Screen):
    def load_collection(self, path):
        """ Summary
            -------
            Called upon the user clicking on the "Load" button.
            Gets the path chosen with the FileChooser and feeds it to
            the app main module to open the collection.
        """
        # get the app, so we can call one of its methods
        app = App.get_running_app()
        app.load_collection(path)
    
    def get_home_directory(self):
        """ Summary
            -------
            Gets the path to the home directory, on all OS. We use it to
            make it so that the FileChooser opens this directory instead
            of the root of the disk

            Returns
            -------
            str
                path to the user's home directory
        """
        return str(Path.home())