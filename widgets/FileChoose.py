
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ListProperty
from plyer import filechooser


class FileChoose(Button):
    '''
    Button that triggers 'filechooser.choose_dir()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def choose(self):
        """
        Call plyer filechooser API to run a filechooser Activity.
        """
        filechooser.choose_dir(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        """
        Callback function for handling the selection response from Activity.
        """
        self.selection = selection

    def on_selection(self, *a, **k):
        """
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        """
        # open the first directory selected (comes as an array)
        path = str(self.selection[0])
        app = App.get_running_app()
        app.load_collection(path)