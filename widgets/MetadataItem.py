from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
import kivy.properties as kyprops

from kivymd.uix.textfield import MDTextField

class MetadataItem(MDTextField):
    field_name = kyprops.StringProperty("")
    title = kyprops.StringProperty("")

    Builder.load_file("templates/MetadataItem.kv")
