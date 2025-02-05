import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame
from pathlib import Path
import fantas
from fantas import uimanager as u
import my_serial
my_serial.start_connect()
from style import *

u.init((800, 800), r=1)
u.images = fantas.load_res_group(Path('./res/images/').iterdir())
u.fonts = fantas.load_res_group(Path('./res/fonts/').iterdir())
u.sounds = fantas.load_res_group(Path('./res/sounds/').iterdir())

pygame.display.set_caption('简易电子琴上位机 -> Written By Fantastair')
pygame.display.set_icon(u.images['icon'])

import init_page
import main_page

main_page.go_back = init_page.go_back
u.root = main_page.root

# init_page.start()
main_page.ani1()

def quit():
    import sys
    pygame.quit()
    my_serial.close_serial()
    sys.exit()

u.mainloop(quit)
