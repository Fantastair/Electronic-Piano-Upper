import fantas
from fantas import uimanager as u

from style import *

import piano

root = fantas.Root(None)


down_board = fantas.Label((u.WIDTH, u.HEIGHT // 2), bg=LIGHTBROWN, topleft=(0, u.HEIGHT))
down_board_pos_kf = fantas.RectKeyFrame(down_board, 'top', u.HEIGHT // 2, 20, u.harmonic_curve)

fantas.Label((u.WIDTH, 4), bg=DEEPBLUE, topleft=(0, 0)).join(down_board)

for i in range(8):
    piano.PianoKey(i, midtop=(113 + 82 * i, -4)).join(down_board)

up_board = fantas.Label((u.WIDTH, u.HEIGHT // 2), bg=LIGHTBLUE, bottomleft=(0, 0))
up_board_pos_kf = fantas.RectKeyFrame(up_board, 'bottom', u.HEIGHT // 2, 20, u.harmonic_curve)
fantas.Label((u.WIDTH, 4), bg=DEEPBLUE, bottomleft=(0, u.HEIGHT // 2)).join(up_board)

def ani1():
    down_board.join(u.root)
    up_board.join(u.root)

    down_board_pos_kf.launch()
    up_board_pos_kf.launch()
