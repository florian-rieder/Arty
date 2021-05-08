from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
import kivy.properties as kyprops

class MetadataItem(BoxLayout):
    field_name = ""

    Builder.load_file("templates/MetadataItem.kv")
