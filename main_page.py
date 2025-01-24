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

fantas.Label((48, u.HEIGHT // 2 - 160), 8, DEEPGRAY, DEEPBLUE, {'border_radius': 24}, center=(u.WIDTH - 80, u.HEIGHT // 4)).join(up_board)

class Rocker(fantas.CircleLabel):
    def __init__(self):
        super().__init__(40, LIGHTRED, 8, DEEPBLUE, center=(u.WIDTH - 80, 104))
        fantas.CircleLabel(8, FAKEWHITE, center=(50, 30)).join(self)

        self.bar = fantas.Label((16, 100), bg=GRAY, radius={'border_radius': 8}, midbottom=(u.WIDTH - 80, u.HEIGHT // 4))
        self.bar.anchor = 'midbottom'
        self.bar.join(up_board)
        self.join(up_board)

        self.mousewidget = RockerMouseWidget(self)
        self.mousewidget.apply_event()
        
        self.free = True

        self.pos_down_kf = fantas.RectKeyFrame(self, 'centery', 296, 10, u.harmonic_curve)
        self.pos_down_kf.bind_endupwith(self.next_board)
        self.pos_up_kf = fantas.RectKeyFrame(self, 'centery', 104, 40, u.slower_curve)
        self.pos_up_kf.bind_endupwith(self.recover_free)

        self.bar_size_kf = fantas.LabelKeyFrame(self.bar, 'size', self.bar.rect.size, 10, u.harmonic_curve)
        self.bar_size_kf_ = fantas.LabelKeyFrame(self.bar, 'size', (self.bar.rect.w, 0), 15, u.harmonic_curve)
        self.bar_size_kf_.bind_endupwith(self.shift)

    def next_board(self):
        self.pos_up_kf.launch('continue')
        self.bar_size_kf_.launch('continue')

    def recover_free(self):
        self.free = True
    
    def shift(self):
        self.bar.rect.midbottom = (u.WIDTH - 80, u.HEIGHT // 4)
        self.bar.anchor = 'midbottom'
        self.bar_size_kf.totalframe = 20
        self.bar_size_kf.launch('continue')

class RockerMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
        self.last_pos = None
    
    def mousepress(self, pos, button):
        if button == self.mousedown == fantas.LEFTMOUSEBUTTON and self.ui.free:
            self.last_pos = pos

    def mouserelease(self, pos, button):
        if button == fantas.LEFTMOUSEBUTTON and self.last_pos is not None:
            if min(max(0, pos[1] - self.last_pos[1]), 192) < 96:
                self.ui.free = False
                self.ui.pos_up_kf.launch('continue')
                self.ui.bar_size_kf.totalframe = 40
                self.ui.bar_size_kf.launch('continue')
            self.last_pos = None

    def mousemove(self, pos):
        if self.last_pos is not None and self.ui.free:
            pos = min(max(0, pos[1] - self.last_pos[1]), 192)
            if pos < 96:
                self.ui.rect.centery = 104 + pos
                self.ui.bar.set_size((16, 200 - self.ui.rect.centery))
            else:
                self.ui.free = False
                self.last_pos = None
                self.ui.pos_down_kf.launch('continue')
                self.ui.bar.rect.midtop = (u.WIDTH - 80, u.HEIGHT // 4)
                self.ui.bar.anchor = 'midtop'
                self.ui.bar_size_kf.totalframe = 10
                self.ui.bar_size_kf.launch('continue')

rocker = Rocker()

control_box = fantas.Label((u.WIDTH - 200, u.HEIGHT // 2 - 80), 8, FAKEWHITE, DEEPBLUE, radius={'border_radius': 32}, topleft=(40, 40))
control_box.join(up_board)
