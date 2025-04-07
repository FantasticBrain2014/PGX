""" PGX.Event, PGX's Event handler.

It has many functions for input from the user.
"""

import arcade
import math

_lastkey = None  # Store the last key pressed
_lastclickpos = None  # Store last mouse click position
_lastclickbutton = None  # Store last mouse button pressed

# Normal keys (without Shift)
_KEY_MAP = {
    arcade.key.A: 'A', arcade.key.B: 'B', arcade.key.C: 'C', arcade.key.D: 'D',
    arcade.key.E: 'E', arcade.key.F: 'F', arcade.key.G: 'G', arcade.key.H: 'H',
    arcade.key.I: 'I', arcade.key.J: 'J', arcade.key.K: 'K', arcade.key.L: 'L',
    arcade.key.M: 'M', arcade.key.N: 'N', arcade.key.O: 'O', arcade.key.P: 'P',
    arcade.key.Q: 'Q', arcade.key.R: 'R', arcade.key.S: 'S', arcade.key.T: 'T',
    arcade.key.U: 'U', arcade.key.V: 'V', arcade.key.W: 'W', arcade.key.X: 'X',
    arcade.key.Y: 'Y', arcade.key.Z: 'Z', arcade.key.KEY_0: '0', arcade.key.KEY_1: '1',
    arcade.key.KEY_2: '2', arcade.key.KEY_3: '3', arcade.key.KEY_4: '4', arcade.key.KEY_5: '5',
    arcade.key.KEY_6: '6', arcade.key.KEY_7: '7', arcade.key.KEY_8: '8', arcade.key.KEY_9: '9',
    
    arcade.key.F1: "F1", arcade.key.F2: "F2", arcade.key.F3: "F3", arcade.key.F4: "F4",
    arcade.key.F5: "F5", arcade.key.F6: "F6", arcade.key.F7: "F7", arcade.key.F8: "F8",
    arcade.key.F9: "F9", arcade.key.F10: "F10", arcade.key.F11: "F11", arcade.key.F12: "F12",

    arcade.key.ESCAPE: "ESC", arcade.key.ENTER: "ENTER", arcade.key.SPACE: "SPACE",
    arcade.key.BACKSPACE: "BACKSPACE", arcade.key.TAB: "TAB", arcade.key.CAPSLOCK: "CAPS LOCK",
    arcade.key.LSHIFT: "SHIFT", arcade.key.RSHIFT: "SHIFT", arcade.key.LCTRL: "CTRL", arcade.key.RCTRL: "CTRL",
    arcade.key.LALT: "ALT", arcade.key.RALT: "ALT", arcade.key.DELETE: "DELETE", arcade.key.INSERT: "INSERT", 
    
    arcade.key.LEFT: "LEFT", arcade.key.RIGHT: "RIGHT", arcade.key.UP: "UP", arcade.key.DOWN: "DOWN",

    arcade.key.MINUS: "-", arcade.key.EQUAL: "=", arcade.key.SEMICOLON: ";",
    arcade.key.APOSTROPHE: "'", arcade.key.COMMA: ",", arcade.key.PERIOD: ".", arcade.key.SLASH: "/",
    arcade.key.BRACKETLEFT: "[", arcade.key.BRACKETRIGHT: "]", arcade.key.BACKSLASH: "\\", arcade.key.GRAVE: "`"
}

# Shifted keys (when holding Shift)
_SHIFTED_KEYS = {
    arcade.key.KEY_1: "!", arcade.key.KEY_2: "@", arcade.key.KEY_3: "#",
    arcade.key.KEY_4: "$", arcade.key.KEY_5: "%", arcade.key.KEY_6: "^",
    arcade.key.KEY_7: "&", arcade.key.KEY_8: "*", arcade.key.KEY_9: "(",
    arcade.key.KEY_0: ")", arcade.key.MINUS: "_", arcade.key.EQUAL: "+",
    arcade.key.SEMICOLON: ":", arcade.key.APOSTROPHE: "\"", arcade.key.COMMA: "<",
    arcade.key.PERIOD: ">", arcade.key.SLASH: "?", arcade.key.BRACKETLEFT: "{",
    arcade.key.BRACKETRIGHT: "}", arcade.key.BACKSLASH: "|", arcade.key.GRAVE: "~"
}

def _on_key_press(key, modifiers):
    """Handles key press events and stores the last key."""
    global _lastkey
    if modifiers & arcade.key.MOD_SHIFT and key in _SHIFTED_KEYS:
        _lastkey = _SHIFTED_KEYS[key]  # Get shifted symbol
    else:
        _lastkey = _KEY_MAP.get(key, None)  # Get normal key

def getkey():
    """Returns the last key pressed and resets it."""
    global _lastkey
    key = _lastkey
    _lastkey = None  # Reset after reading
    return key

def _on_mouse_press(x, y, button, modifiers):
    """Handles mouse clicks and stores the last click position and button."""
    global _lastclickpos, _lastclickbutton
    x2 = int(x)
    y2 = int(y)
    _lastclickpos = (x2, y2)
    _lastclickbutton = button

def click():
    """Returns True if the left mouse button was clicked and resets."""
    global _lastclickbutton
    if _lastclickbutton == arcade.MOUSE_BUTTON_LEFT:
        _lastclickbutton = None  # Reset after reading
        return True
    return False

def rightclick():
    """Returns True if the right mouse button was clicked and resets."""
    global _lastclickbutton
    if _lastclickbutton == arcade.MOUSE_BUTTON_RIGHT:
        _lastclickbutton = None  # Reset after reading
        return True
    return False

def specialclick():
    """Returns True if the middle mouse button was clicked and resets."""
    global _lastclickbutton
    if _lastclickbutton == arcade.MOUSE_BUTTON_MIDDLE:
        _lastclickbutton = None  # Reset after reading
        return True
    return False

def getclickpos():
    """Returns the last click position and resets it."""
    global _lastclickpos
    pos = _lastclickpos
    _lastclickpos = None  # Reset after reading
    return pos

def getclickangle(center_obj):
    """Returns the angle between the last mouse click and a given center point."""
    if _lastclickpos is None:
        return None
    dx = _lastclickpos[0] - center_obj[0]
    dy = _lastclickpos[1] - center_obj[1]
    return math.degrees(math.atan2(dy, dx))

def bind(window):
    """Binds all input handling to a window."""
    window.win.on_key_press = _on_key_press
    window.win.on_mouse_press = _on_mouse_press

__all__ = ['bind', 'click', 'getclickangle', 'getclickpos',
           'getkey', 'rightclick', 'specialclick']
