from kivy.lang import Builder
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.properties import ListProperty

from api.Collection import CollectionImage

class CollectionToolbar(BoxLayout):
    """ Summary
        -------
        Toolbar to access other pages (Comparison).

        Attributes
        ----------

        Methods
        -------

    """
    Builder.load_file('templates/CollectionToolbar.kv')

    selected_images = ListProperty([])

    def compare(self):
        # get selected images
        # send them to the compare screen
        print("compare selection")
        app = App.get_running_app()
        app.SCREENS["COMPARE"].load_images(self.selected_images)
        app.SCREEN_MANAGER.switch_to(app.SCREENS["COMPARE"], direction ='right')
    


    def export(self):
        # get selected images
        # export them
        print("export selection")
        pass
    

    def _get_selected_images(self):
        pass

