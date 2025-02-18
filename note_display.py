import random
import pygame
import fantas
from fantas import uimanager as u
import my_serial
from style import *
import sync

set_piano_volume = None
u.CREATERANDOMNOTE = pygame.event.custom_type()
active = False

def activate():
    global active
    active = True
    pygame.time.set_timer(u.CREATERANDOMNOTE, 400)
activate()
def unactivate():
    global active
    active = False
    pygame.time.set_timer(u.CREATERANDOMNOTE, 0)

board = fantas.fantas.Label((u.WIDTH - 216, u.HEIGHT // 2 - 80))

fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 32)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 64)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 96)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 128)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 160)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 192)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 224)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 256)).join(board)
fantas.Label((520, 1), bg=LIGHTGRAY, topleft=(80, 288)).join(board)
fantas.Label((80, u.HEIGHT // 2 - 88), bg=WHITEGREEN, topleft=(0, 4)).join(board)
fantas.Label((8, u.HEIGHT // 2 - 88), bg=DEEPBLUE, midtop=(80, 4)).join(board)
volume_bar_box = fantas.Label((38, u.HEIGHT // 2 - 120), 4, FAKEWHITE, DEEPGREEN, {'border_radius': 4}, center=(40, u.HEIGHT // 4 - 40))
volume_bar_box.join(board)
fantas.Label((30, 4), bg=DEEPGREEN, midleft=(4, 56)).join(volume_bar_box)
fantas.Label((30, 4), bg=DEEPGREEN, midleft=(4, 111)).join(volume_bar_box)
fantas.Label((30, 4), bg=DEEPGREEN, midleft=(4, 165)).join(volume_bar_box)
fantas.Label((30, 4), bg=DEEPGREEN, midleft=(4, 220)).join(volume_bar_box)

volume_bar = fantas.Label((30, 0), bg=LIGHTGREEN, bottomleft=(4, 276))
volume_bar.anchor = 'midbottom'
volume_bar.join_to(volume_bar_box, 0)
vb_size_kf = fantas.LabelKeyFrame(volume_bar, 'size', (30, 0), 8, u.slower_curve)

volume_cursor = fantas.IconText(chr(0xe708), u.fonts['iconfont'], vb_cursor_style, center=(volume_bar_box.rect.centerx, volume_bar_box.rect.bottom - 6))
volume_cursor.join(board)
vc_pos_kf = fantas.RectKeyFrame(volume_cursor, 'centery', 0, 8, u.slower_curve)

def cursor_jump():
    if not vc_pos_kf.is_launched() and volume != 0:
        if vc_pos_kf.curve != u.parabola1_curve:
            vc_pos_kf.curve = u.parabola1_curve
        vc_pos_kf.value = volume_cursor.rect.centery - 20
        vc_pos_kf.launch('continue')

volume = 0
def set_volume(value, from_sync=False):
    global volume
    t = min(max(value, 0), 5)
    if volume != t:
        volume = t
        if vc_pos_kf.curve != u.slower_curve:
            vc_pos_kf.curve = u.slower_curve
        vc_pos_kf.value = volume_bar_box.rect.bottom - round(272 * volume / 5) - 6
        vc_pos_kf.launch('continue')
        set_piano_volume((volume / 5) ** 2)
        if not from_sync:
            my_serial.send_write_order([0x01, t])
        if volume == 0 and active:
            unactivate()
        elif not active:
            activate()

def sync_volume(value):
    set_volume(value[0], True)
sync.SyncTrigger('volume', sync_volume)

def get_volume():
    return volume
u.get_volume = get_volume

class VolumeBarBoxMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 3)
    
    def pos2volume(self, pos):
        return 5 - min(max(pos, 0), 280) // 56

    def mousepress(self, pos, button):
        if button == self.mousedown == fantas.LEFTMOUSEBUTTON:
            set_volume(self.pos2volume(pos[1]))
    
    def mousemove(self, pos):
        if self.mousedown == fantas.LEFTMOUSEBUTTON:
            set_volume(self.pos2volume(pos[1]))
    
    def mousescroll(self, x, y):
        if self.mouseon:
            set_volume(volume + y)
    
    def handle(self, event):
        super().handle(event)
        if event.type == u.CREATERANDOMNOTE:
            RandomNote()


VolumeBarBoxMouseWidget(volume_bar_box).apply_event()

class RandomNote(fantas.IconText):
    def __init__(self):
        random_style = {
            'fgcolor': WHITEGREEN,
            'size': random.randint(-16, 96) + 64,
            'rotation': random.randint(-30, 30),
        }
        random_pos = (u.WIDTH - 216, random.randint(20, 300))
        super().__init__(chr(random.randint(0xe600, 0xe60a)), u.fonts['iconfont'], random_style, midleft=random_pos)
        kf = fantas.RectKeyFrame(self, 'right', 80, random.randint(120, 300), u.curve)
        kf.launch()
        kf.bind_endupwith(self.leave)
        self.join_to(board, 0)

class PlayNote(fantas.Label):
    def __init__(self, note_num):
        super().__init__((32, 32), bg=note_color_family[note_num], radius={'border_radius': 16}, midleft=(u.WIDTH - 216, 272 - note_num * 32))
        self.join_to(board, -4)
        self.anchor = 'midright'
        if note_num < 4:
            note_text_style['fgcolor'] = DEEPBLUE
        else:
            note_text_style['fgcolor'] = FAKEWHITE
        fantas.Text(str(note_num % 7 + 1), u.fonts['shuhei'], note_text_style, center=(16, 15)).join(self)
        if note_num == 7:
            fantas.CircleLabel(2, FAKEWHITE, center=(17, 4)).join(self)
        self.pos_kf = fantas.RectKeyFrame(self, 'right', u.WIDTH - 216, 12, u.harmonic_curve)
        self.pos_kf.bind_endupwith(self.ready)
        self.size_kf = fantas.LabelKeyFrame(self, 'size', (16 + 3580 * 32, 32), 3600 * 10, u.curve)
        self.pos_kf.launch()

    def ready(self):
        self.size_kf.launch()

    def go(self):
        if self.size_kf.is_launched():
            self.size_kf.stop()
        self.smooth_go()

    def smooth_go(self):
        self.pos_kf.value -= 560
        self.pos_kf.curve = u.curve
        self.pos_kf.totalframe = 180
        self.pos_kf.launch('continue')
        self.pos_kf.bind_endupwith(self.leave)

playing_num = 0
playing_notes = [None] * 8
def play_sound(note_num):
    global playing_num
    playing_num += 1
    vb_size_kf.value = (30, round(volume / 5 * 272))
    vb_size_kf.totalframe = 6
    vb_size_kf.curve = u.faster_curve
    vb_size_kf.bind_endupwith(cursor_jump)
    vb_size_kf.launch('continue')
    playing_notes[note_num] = PlayNote(note_num)

def unplay_sound(note_num):
    global playing_num
    playing_num -= 1
    if playing_num == 0:
        vb_size_kf.value = (30, 0)
        vb_size_kf.totalframe = 15
        vb_size_kf.curve = u.slower_curve
        vb_size_kf.bind_endupwith(None)
        vb_size_kf.launch('continue')
    playing_notes[note_num].go()
