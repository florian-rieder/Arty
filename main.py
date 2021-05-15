import os
import platform

from kivy.config import Config
from kivy.logger import Logger

from ArtyApp import ArtyApp

# I don't really know what it does, but it could be useful later
# def reset():
#     import kivy.core.window as window
#     from kivy.base import EventLoop
#     if not EventLoop.event_listeners:
#         from kivy.cache import Cache
#         window.Window = window.core_select_lib('window', window.window_impl, True)
#         Cache.print_usage()
#         for cat in Cache._categories:
#             Cache._objects[cat] = {}

if __name__ == '__main__':
    #reset()
    log_dir = os.path.join(os.path.expanduser("~/Documents"), "Arty", "logs")

    #========================= Configuration =========================#

    # set default size and minimum size of the window
    Config.set('graphics',  'width',            '1200')
    Config.set('graphics',  'height',           '800')
    Config.set('graphics',  'minimum_width',    '800')
    Config.set('graphics',  'minimum_height',   '600')

    # prevent quitting when ESCAPE is pressed
    Config.set('kivy',      'exit_on_escape',   '0')

    # logging config: we send the logs to our own folder
    Config.set('kivy',      'log_dir',          log_dir)
    Config.set('kivy',      'log_name',         r'arty_%y-%m-%d_%_.txt')
    Config.set('kivy',      'log_maxfiles',     5)

    # prevent red dots on right click
    Config.set('input',     'mouse',            'mouse, disable_multitouch')

    # apply configuration
    Config.write()

    #======================= End Configuration =======================#

    # run the app
    ArtyApp().run()
