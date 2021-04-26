from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

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

    def compare(self):
        # get selected images
        # send them to the compare screen
        print("compare selection")
        pass


    def export(self):
        # get selected images
        # export them
        print("export selection")
        pass
    

    def _get_selected_images(self):
        pass