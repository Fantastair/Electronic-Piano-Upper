import pygame
import fantas
from fantas import uimanager as u
from style import *

import numpy as np
from scipy import signal

class PianoKeyMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
    
    def mousein(self):
        self.ui.color_dark_kf.launch('continue')

    def mouseout(self):
        self.ui.color_light_kf.launch('continue')
    
    def mousepress(self, pos, button):
        if button == 1 and self.mouseon:
            self.ui.play()
    
    def mouserelease(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.unplay()

class PianoKeyKeyBoardWidget(fantas.KeyboardBase):
    def keyboardpress(self, key, shortcut):
        if key == self.ui.key:
            self.ui.play()

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
        self.color_dark_kf = fantas.LabelKeyFrame(self, 'bg', self.bg - color_offset, 10, u.curve)
        self.color_light_kf = fantas.LabelKeyFrame(self, 'bg', self.bg, 10, u.curve)

        sample_rate = 44100
        t = np.linspace(0, 1, int(sample_rate), False)
        # wave = np.sin(2 * np.pi * self.freq * t)
        wave = signal.square(2 * np.pi * self.freq * t)
        sound_array = np.ascontiguousarray(np.array([32767 * wave, 32767 * wave]).T.astype(np.int16))
        self.sound = pygame.sndarray.make_sound(sound_array)

    def play(self):
        self.num_text_pos_down_kf.launch('continue')
        self.size_long_kf.launch('continue')
        if self.num >= 7:
            self.high_point_pos_down_kf.launch('continue')
        self.sound.play(loops=-1, fade_ms=50)

    def unplay(self):
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
