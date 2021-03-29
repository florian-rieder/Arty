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
    ArtyApp().run()