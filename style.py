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

note_color_family = (
    pygame.Color('#ddffe9'),
    pygame.Color('#c1eade'),
    pygame.Color('#a4c6b7'),
    pygame.Color('#88b3b1'),
    pygame.Color('#769fa5'),
    pygame.Color('#577c86'),
    pygame.Color('#486a77'),
    pygame.Color('#2f4858'),
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
music_name_style = get_text(36, DEEPBLUE)
memory_text_style = get_text(42, DEEPBLUE)
ml_button_text_style = get_text(48, FAKEWHITE)
mlub_button_text_style = get_text(24, DEEPBLUE)
mlub_tip_text_style = get_text(36, DEEPBLUE)

memory_button_color = {
    'origin_bg': FAKEWHITE,
    'hover_bg': FAKEWHITE + color_offset,
    'press_bg': FAKEWHITE - color_offset,
    'origin_bd': 2,
    'hover_bd': 4,
    'press_bd': 4,
    'origin_sc': DEEPBLUE,
    'hover_sc': DEEPBLUE,
    'press_sc': DEEPBLUE,
}
ml_button_color = {
    'origin_bg': DEEPBLUE,
    'hover_bg': DEEPBLUE,
    'press_bg': DEEPBLUE,
    'origin_bd': 0,
    'hover_bd': 0,
    'press_bd': 0,
    'origin_sc': None,
    'hover_sc': None,
    'press_sc': None,
}
mlub_button_color = {
    'origin_bg': FAKEWHITE,
    'hover_bg': FAKEWHITE + color_offset,
    'press_bg': FAKEWHITE - color_offset,
    'origin_bd': 2,
    'hover_bd': 4,
    'press_bd': 4,
    'origin_sc': DEEPBLUE,
    'hover_sc': DEEPBLUE,
    'press_sc': DEEPBLUE,
}

del pygame, u
