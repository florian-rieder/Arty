from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
import kivy.properties as kyprops

class FilterDropdown(DropDown):
    """ Summary
        -------
        Dropdown list for the filter options

        Attributes
        ----------

        Methods:
        --------
    """

    Builder.load_file('templates/FilterDropdown.kv')
    # state = kyprops.BooleanProperty(False)