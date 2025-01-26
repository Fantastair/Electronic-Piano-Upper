import random
import pygame
import fantas
from fantas import uimanager as u

import note_display

from style import *

import my_serial


class PianoKeyMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
    
    def mousein(self):
        self.ui.color_kf.value = FAKEWHITE - color_offset
        self.ui.color_kf.launch('continue')

    def mouseout(self):
        self.ui.color_kf.value = FAKEWHITE
        self.ui.color_kf.launch('continue')

    def mousepress(self, pos, button):
        if button == 1 and self.mouseon:
            self.ui.play()
            Note(pygame.mouse.get_pos())
    
    def mouserelease(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.unplay()

class PianoKeyKeyBoardWidget(fantas.KeyboardBase):
    def keyboardpress(self, key, shortcut):
        if key == self.ui.key:
            self.ui.play()
            Note((self.ui.rect.centerx + self.ui.father.rect.left, self.ui.rect.centery + self.ui.father.rect.top))

    def keyboardrelease(self, key, shortcut):
        if key == self.ui.key:
            self.ui.unplay()
    
class PianoKey(fantas.Label):
    freq_map = (523, 587, 659, 698, 784, 880, 988, 1046)
    key_map = ('1', '2', '3', '4', '5', '6', '7', '8')

    def __init__(self, num, **anchor):
        super().__init__((90, 320), 8, FAKEWHITE, DEEPBLUE, {'border_bottom_left_radius': 16, 'border_bottom_right_radius': 16}, **anchor)
        self.num = num
        self.freq = self.freq_map[num]
        self.key = self.key_map[num]
        self.anchor = 'midtop'
        self.played = False

        self.mousewidget = PianoKeyMouseWidget(self)
        self.mousewidget.apply_event()
        self.keyboardwidget = PianoKeyKeyBoardWidget(self)
        self.keyboardwidget.apply_event()

        self.num_text = fantas.Text(str(num % 7 + 1), u.fonts['shuhei'], piano_num_text_style, center=(self.rect.w // 2, self.rect.bottom - 32))
        self.num_text.join(self)
        self.num_text_pos_down_kf = fantas.RectKeyFrame(self.num_text, 'centery', self.rect.bottom - 20, 10, u.harmonic_curve)
        self.num_text_pos_up_kf = fantas.RectKeyFrame(self.num_text, 'centery', self.rect.bottom - 32, 10, u.harmonic_curve)

        if num >= 7:
            self.high_point = fantas.CircleLabel(4, DEEPBLUE, center=(self.rect.w // 2 + 2, self.rect.bottom - 52))
            self.high_point.join(self)
            self.high_point_pos_down_kf = fantas.RectKeyFrame(self.high_point, 'centery', self.rect.bottom - 40, 10, u.harmonic_curve)
            self.high_point_pos_up_kf = fantas.RectKeyFrame(self.high_point, 'centery', self.rect.bottom - 52, 10, u.harmonic_curve)

        self.size_long_kf = fantas.LabelKeyFrame(self, 'size', (self.rect.w, self.rect.h + 12), 10, u.harmonic_curve)
        self.size_short_kf = fantas.LabelKeyFrame(self, 'size', (self.rect.w, self.rect.h), 10, u.harmonic_curve)
        self.color_kf = fantas.LabelKeyFrame(self, 'bg', self.bg - color_offset, 10, u.curve)
        self.sound = pygame.mixer.Sound(generate_square(self.freq))

    def play(self):
        if not self.played:
            self.num_text_pos_down_kf.launch('continue')
            self.size_long_kf.launch('continue')
            if self.num >= 7:
                self.high_point_pos_down_kf.launch('continue')
            self.sound.play(loops=-1)
            my_serial.send_write_order([0x00, 0x00, self.num])
            self.played = True
            if note_display.active:
                note_display.play_sound(self.num)

    def unplay(self):
        if self.played:
            if self.num_text_pos_down_kf.is_launched():
                self.num_text_pos_down_kf.stop()
            self.num_text_pos_up_kf.launch('continue')
            if self.size_long_kf.is_launched():
                self.size_long_kf.stop()
            self.size_short_kf.launch('continue')
            if self.num >= 7:
                if self.high_point_pos_down_kf.is_launched():
                    self.high_point_pos_down_kf.stop()
                self.high_point_pos_up_kf.launch('continue')
            self.sound.fadeout(500)
            my_serial.send_write_order([0x00, 0x01, self.num])
            self.played = False
            if note_display.active:
                note_display.unplay_sound(self.num)
    
    def set_volume(self, value):
        self.sound.set_volume(value)

class Note(fantas.IconText):
    def __init__(self, pos_ref):
        random_style = {
            'fgcolor': random.choice(u.random_color_family),
            'size': random.randint(-10, 10) + 36,
            'rotation': random.randint(-20, 20),
        }
        random_center = (pos_ref[0] + random.randint(-20, 20), pos_ref[1] + random.randint(-20, 20))
        super().__init__(chr(random.randint(0xe600, 0xe609)), u.fonts['iconfont'], random_style, center=random_center)
        self.join(u.root)
        random_frame = random.randint(15, 25)
        random_alpha_kf = fantas.UiKeyFrame(self, 'alpha', 0, random_frame, u.curve)
        random_alpha_kf.bind_endupwith(self.leave)
        random_pos_kf = fantas.RectKeyFrame(self, 'centery', random_center[1] - random.randint(30, 60), random_frame, u.faster_curve)
        random_alpha_kf.launch()
        random_pos_kf.launch()

def generate_square(freq):
    sample_rate = 44100
    l = sample_rate // freq
    if l % 2 != 0:
        l -= 1
    result = [b'\xff\x7f' * l, b'\x01\x80' * l] * freq
    l, s = freq * 2, sample_rate - len(b''.join(result)) // 4
    temp = [0] * l
    interval = l // s
    remainder = l % s
    pos = 0
    for i in range(s):
        temp[pos] = 1
        pos += interval + (1 if i < remainder else 0)
    for i in range(l):
        if temp[i] == 1:
            result[i] += result[i][:4]
    return b''.join(result)
