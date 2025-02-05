import pygame
import pygame.freetype

from fantas import uimanager as u
u.random_color_family = (
    pygame.Color('#845ec2'),
    pygame.Color('#d65db1'),
    pygame.Color('#ff6f91'),
    pygame.Color('#ff9671'),
    pygame.Color('#ffc75f'),
    pygame.Color('#f9f871'),
    pygame.Color('#2c73d2'),
    pygame.Color('#008f7a'),
    pygame.Color('#fbeaff'),
    pygame.Color('#b39cd0'),
    pygame.Color('#00c9a7'),
    pygame.Color('#c34a36'),
    pygame.Color('#4ffbdf'),
)

def get_color(value):
    return pygame.Color('#' + value)

def get_text(size, color):
    return {'size': size, 'fgcolor': color}

BLACK = get_color('000000')
WHITE = get_color('ffffff')
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
LIGHTGREEN = get_color('9cd498')
WHITEGREEN = get_color('ddffe9')
DEEPGREEN = get_color('6ca171')

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
vb_cursor_style = get_text(72, BLACK)
vb_cursor_style['rotation'] = 90
note_text_style = get_text(24, DEEPBLUE)
record_note_text_style = get_text(144, FAKEWHITE - color_offset)

del pygame, u
