from kivy.config import Config

from ArtyApp import ArtyApp

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

    # Configuration

    # set min and max size of the window
    Config.set('graphics',  'width',            '1200')
    Config.set('graphics',  'height',           '800')
    Config.set('graphics',  'minimum_width',    '800')
    Config.set('graphics',  'minimum_height',   '600')

    # prevent quitting when ESCAPE is pressed
    Config.set('kivy',      'exit_on_escape',   '0')

    # apply configuration
    Config.write()

    # run the app
    ArtyApp().run()