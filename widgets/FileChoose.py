
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from plyer import filechooser


class FileChoose(Button):
    """
        Button that triggers 'filechooser.choose_dir()' and processes
        the data response from filechooser Activity.
    """

    def choose(self):
        """
            Call plyer filechooser API to run a filechooser Activity.
        """
        filechooser.choose_dir(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        """
            Callback function for handling the selection response from Activity.
        """

        if not selection:
            Logger.info("Arty: No path selected.")
            return

        Logger.info("Arty: Loading collection from chooser...")
        # open the first directory selected (comes as an array)
        path = str(selection[0])

        app = App.get_running_app()
        app.load_collection(path)
