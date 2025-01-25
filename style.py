import pygame
import pygame.freetype

def get_color(value):
    return pygame.Color('#' + value)

def get_text(size, color):
    return {'size': size, 'fgcolor': color}

FAKEWHITE = get_color('e3e3e3')
DEEPBLUE = get_color('4a466e')
LIGHTBROWN = get_color('e6c28e')
LIGHTBLUE = get_color('a8cceb')
LIGHTRED = get_color('d6707c')
DEEPGRAY = get_color('202020')
GRAY = get_color('888888')
LIGHTGRAY = get_color('bbbbbb')
DARKGRAY = get_color('555555')
DARKRED = get_color('b4666f')

color_offset = get_color('32323200')

stm32_text_style = get_text(48, DEEPBLUE)
init_info_style = get_text(48, DEEPBLUE)
tip_text_style = get_text(36, LIGHTRED)
piano_num_text_style = get_text(36, DEEPBLUE)
about_big_text_style = get_text(36, DEEPBLUE)
about_middle_text_style = get_text(24, DEEPBLUE)
about_small_text_style = get_text(16, DEEPBLUE)
virtual_button_text_style = get_text(28, FAKEWHITE)
vb_tip_text_style = get_text(48, DEEPBLUE)
vb_info_text_style = get_text(28, DEEPBLUE)

del pygame
