import fantas
from style import *

class PianoKey(fantas.Label):
    def __init__(self, **anchor):
        super().__init__((90, 320), 8, FAKEWHITE, DEEPBLUE, {'border_bottom_left_radius': 16, 'border_bottom_right_radius': 16}, **anchor)
