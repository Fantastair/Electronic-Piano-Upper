import fantas
from fantas import uimanager as u
import piano
import virtual_key

from style import *


root = fantas.Root(None)


down_board = fantas.Label((u.WIDTH, u.HEIGHT // 2), bg=LIGHTBROWN, topleft=(0, u.HEIGHT))
down_board_pos_kf = fantas.RectKeyFrame(down_board, 'top', u.HEIGHT // 2, 20, u.harmonic_curve)

fantas.Label((u.WIDTH, 4), bg=DEEPBLUE, topleft=(0, 0)).join(down_board)

piano_keys = []
for i in range(8):
    piano_keys.append(piano.PianoKey(i, midtop=(113 + 82 * i, -4)))
    piano_keys[-1].join(down_board)

go_back = None
class DownBoardWidget(fantas.Widget):
    def handle(self, event):
        if event.type == u.UNCONNECTEVENT:
            for k in piano_keys:
                k.unplay()
            for k in virtualkeys:
                if k.pushed:
                    k.release()
            go_back()
DownBoardWidget(down_board).apply_event()

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
            subpallets[(subpallet + 1) % len(subpallets)].rect.top = 320
            subpallets[(subpallet + 1) % len(subpallets)].join(pallet)

    def mouserelease(self, pos, button):
        if button == fantas.LEFTMOUSEBUTTON and self.last_pos is not None:
            if round(min(max(0, pos[1] - self.last_pos[1]), 192) ** 0.8675) < 96:
                self.ui.free = False
                self.ui.pos_up_kf.launch('continue')
                self.ui.bar_size_kf.totalframe = 40
                self.ui.bar_size_kf.launch('continue')
                pallet_pos_down_kf.launch('continue')
            self.last_pos = None

    def mousemove(self, pos):
        if self.last_pos is not None and self.ui.free:
            pos = round(min(max(0, pos[1] - self.last_pos[1]), 192) ** 0.8675)
            if pos < 96:
                self.ui.rect.centery = 104 + pos
                self.ui.bar.set_size((16, 200 - self.ui.rect.centery))
                pallet.rect.top = -pos
                pallet.father.mark_update()
            else:
                self.ui.free = False
                self.last_pos = None
                self.ui.pos_down_kf.launch('continue')
                self.ui.bar.rect.midtop = (u.WIDTH - 80, u.HEIGHT // 4)
                self.ui.bar.anchor = 'midtop'
                self.ui.bar_size_kf.totalframe = 10
                self.ui.bar_size_kf.launch('continue')
                u.sounds['drag_bar'].play()
                pallet_pos_up_kf.launch('continue')

rocker = Rocker()

control_box = fantas.Label((u.WIDTH - 200, u.HEIGHT // 2 - 80), 8, FAKEWHITE, DEEPBLUE, radius={'border_radius': 32}, topleft=(40, 40))
control_box.join(up_board)

pallet = fantas.Label((u.WIDTH - 264, u.HEIGHT - 160), topleft=(32, 0))
pallet.join(control_box)

pallet_pos_up_kf = fantas.RectKeyFrame(pallet, 'centery', 0, 40, u.rebound_curve)
pallet_pos_down_kf = fantas.RectKeyFrame(pallet, 'top', 0, 40, u.harmonic_curve)

def after_up():
    global subpallet
    subpallets[subpallet].leave()
    subpallet = (subpallet + 1) % len(subpallets)
    subpallets[subpallet].rect.top = 0
    pallet.rect.top = 0
    pallet.mark_update()
pallet_pos_up_kf.bind_endupwith(after_up)

def after_down():
    subpallets[(subpallet + 1) % len(subpallets)].leave()
pallet_pos_down_kf.bind_endupwith(after_down)

fantas.Label((u.WIDTH - 300, 8), bg=LIGHTGRAY, radius={'border_radius': 4}, center=(u.WIDTH // 2 - 132, u.HEIGHT // 2 - 80)).join(pallet)
fantas.Label((u.WIDTH - 300, 8), bg=LIGHTGRAY, radius={'border_radius': 4}, midbottom=(u.WIDTH // 2 - 132, u.HEIGHT - 160)).join(pallet)
fantas.Label((u.WIDTH - 264, 8), bg=DEEPBLUE, midtop=(u.WIDTH // 2 - 100, 0)).join(control_box)
fantas.Label((u.WIDTH - 264, 8), bg=DEEPBLUE, midbottom=(u.WIDTH // 2 - 100, u.HEIGHT // 2 - 80)).join(control_box)

virtual_button_box = fantas.fantas.Label((u.WIDTH - 264, u.HEIGHT // 2 - 80))
# note_display_box = fantas.fantas.Label((u.WIDTH - 264, u.HEIGHT // 2 - 80))

subpallets = [
    # note_display_box,
    virtual_button_box,
    fantas.fantas.Label((u.WIDTH - 264, u.HEIGHT // 2 - 80)),
]

subpallet = 0

subpallets[subpallet].rect.topleft = (0, 0)
subpallets[subpallet].join(pallet)
subpallets[(subpallet + 1) % len(subpallets)].rect.topleft = (0, 320)

fantas.Text('简易电子琴 - 上位机', u.fonts['deyi'], about_big_text_style, midleft=(0, 40)).join(subpallets[-1])
fantas.Text('2025 山东大学寒假 STM32 系统设计大赛小组作品', u.fonts['deyi'], about_middle_text_style, midleft=(0, 82)).join(subpallets[-1])
fantas.Text('组名：不会弹琴的电阻', u.fonts['deyi'], about_middle_text_style, midleft=(0, 108)).join(subpallets[-1])
i = fantas.Ui(u.images['icon'], center=(480, 70))
i.size = (96, 96)
i.apply_size()
i.join(subpallets[-1])
k = fantas.UiKeyFrame(i, 'angle', 0, 60, u.slower_curve)
a = fantas.AnyButton(i)
def ani2(kf, ui):
    ui.angle -= 360
    kf.launch('continue')
a.bind(ani2, k, i)
a.apply_event()

fantas.Text('版本号：V0.7.1', u.fonts['deyi'], about_middle_text_style, midleft=(0, 152)).join(subpallets[-1])
fantas.Text('适用下位机固件版本：V0.5', u.fonts['deyi'], about_middle_text_style, midleft=(0, 180)).join(subpallets[-1])

fantas.Text('程序语言：python 3.12.7', u.fonts['deyi'], about_middle_text_style, midleft=(0, 216)).join(subpallets[-1])
fantas.Text('开源协议：MIT license', u.fonts['deyi'], about_middle_text_style, midleft=(0, 244)).join(subpallets[-1])
fantas.Text('--- 第三方库 ---', u.fonts['deyi'], about_middle_text_style, midleft=(320, 152)).join(subpallets[-1])
fantas.Text('pygame', u.fonts['deyi'], about_middle_text_style, midleft=(320, 180)).join(subpallets[-1])
fantas.Text('pyserial', u.fonts['deyi'], about_middle_text_style, midleft=(320, 204)).join(subpallets[-1])
fantas.Text('numpy', u.fonts['deyi'], about_middle_text_style, midleft=(320, 228)).join(subpallets[-1])
fantas.Text('scipy', u.fonts['deyi'], about_middle_text_style, midleft=(320, 252)).join(subpallets[-1])
fantas.Text('2.6.1', u.fonts['deyi'], about_middle_text_style, midright=(450, 180)).join(subpallets[-1])
fantas.Text('3.5', u.fonts['deyi'], about_middle_text_style, midright=(450, 204)).join(subpallets[-1])
fantas.Text('2.2.2', u.fonts['deyi'], about_middle_text_style, midright=(450, 228)).join(subpallets[-1])
fantas.Text('1.15.1', u.fonts['deyi'], about_middle_text_style, midright=(450, 252)).join(subpallets[-1])

fantas.WebURL('Github - 源代码仓库', 'https://github.com/Fantastair/Electronic-Piano-Upper', u.fonts['deyi'], about_small_text_style, midleft=(24, 296)).join(subpallets[-1])
fantas.WebURL('Win64位 - 稳定版发布', '#', u.fonts['deyi'], about_small_text_style, midleft=(196, 296)).join(subpallets[-1])
fantas.WebURL('Github - 下位机固件', 'https://github.com/Fantastair/Simple-Electronic-Keyboard', u.fonts['deyi'], about_small_text_style, midleft=(384, 296)).join(subpallets[-1])

fantas.Text('虚拟按键', u.fonts['shuhei'], vb_tip_text_style, center=(267, 48)).join(virtual_button_box)

virtualkeys = [
    virtual_key.VirtualKey('+', '音量 +', 12, center=(48, 140)),
    virtual_key.VirtualKey('-', '音量 -', 13, center=(48, 240)),
    virtual_key.VirtualKey('+', '菜单 +', 15, center=(486, 140)),
    virtual_key.VirtualKey('-', '菜单 -', 14, center=(486, 240)),
    virtual_key.VirtualKey('1', '操作 1', 11, center=(156, 240)),
    virtual_key.VirtualKey('2', '操作 2', 10, center=(230, 240)),
    virtual_key.VirtualKey('3', '操作 3', 9, center=(304, 240)),
    virtual_key.VirtualKey('4', '操作 4', 8, center=(378, 240)),
]
for k in virtualkeys:
    k.join(virtual_button_box)
virtual_key.info_box.join(virtual_button_box)
