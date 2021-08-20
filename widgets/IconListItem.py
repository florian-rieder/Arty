from kivy.lang import Builder
import kivy.properties as kyprops

from kivymd.uix.list import OneLineIconListItem

class IconListItem(OneLineIconListItem):
    Builder.load_file('templates/IconListItem.kv')
    icon = kyprops.StringProperty()
