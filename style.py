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

stm32_text_style = get_text(48, DEEPBLUE)
init_info_style = get_text(48, DEEPBLUE)
tip_text_style = get_text(36, LIGHTRED)

del pygame, get_color, get_text
