from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import kivy.properties as kyprops

class FilterPopup(BoxLayout):
    """ Summary
        -------
        Dropdown list for the filter options

        Attributes
        ----------

        Methods:
        --------
    """

    Builder.load_file('templates/FilterPopup.kv')