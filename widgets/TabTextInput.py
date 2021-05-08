from kivy.uix.textinput import TextInput


class TabTextInput(TextInput):
    """ Summary
        -------
        Custom TextInput class that allows for switching between
        TextInputs using Tab or Enter.

        Methods
        -------
        set_next(next_field):
            Set the element to switch focus to when Tab or Enter is
            pressed.
    """

    def __init__(self, *args, **kwargs):
        # This allows you to pass next when you instantiate the input, or 
        # alternatively call set_next on an existing input.
        self.next = kwargs.pop('next', None)
        self.write_tab = False
        super(TabTextInput, self).__init__(*args, **kwargs)


    def set_next(self, next_field):
        """ Summary
            -------
            Set the element to switch focus to when Tab or Enter is
            pressed.

            Arguments
            ---------
            next_field : focusable kivy widget
                Any kivy widget which can be focused. (for instance,
                another TabTextInput)
        """
        self.next = next_field


    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, _key_str = keycode
        # 9 and 13 are the key codes for tab and enter.
        if key in (9, 13) and self.next is not None:
            self.next.focus = True
            self.next.select_all()
        else:
            super(TabTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
