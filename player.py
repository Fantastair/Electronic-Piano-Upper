import pygame.freetype
import fantas
from fantas import uimanager as u
import sync
import my_serial
from style import *

board = fantas.fantas.Label((u.WIDTH - 216, u.HEIGHT // 2 - 80))

record = fantas.CircleLabel(120, DEEPGRAY, 8, LIGHTRED, center=(160, 160))
record.join(board)
fantas.CircleLabel(48, DARKGRAY, center=(120, 120)).join(record)
record_note = fantas.IconText(chr(0xe605), u.fonts['iconfont'], record_note_text_style, center=(120, 120))
record_note.join(record)
record_angle_kf = fantas.UiKeyFrame(record_note, 'angle', 360, 360, u.curve)
record_angle_kf.launch('continue')
record_angle_kf.stop()
fantas.CircleLabel(12, LIGHTRED, center=(120, 120)).join(record)

arm = fantas.Label((85, 200), topright=(370, -10))
arm.anchor = 'topright'
arm.angle = 30
arm.join(board)
arm_pos_kf = fantas.RectKeyFrame(arm, 'topright', (0, 0), 10, u.slower_curve)
arm_angle_kf = fantas.UiKeyFrame(arm, 'angle', 10, 30, u.slower_curve)
fantas.Label((12, 140), bg=DEEPBLUE, radius={'border_radius': 6}, topright=(72, 0)).join(arm)
arm_head = fantas.Label((36, 90), 6, DARKRED, DEEPBLUE, radius={'border_radius': 18}, bottomleft=(0, 200))
arm_head.anchor = 'bottomleft'
arm_head.angle = -45
arm_head.join(arm)
point_led = fantas.CircleLabel(6, DEEPBLUE, center=(18, 72))
point_led.join(arm_head)
bar_led = fantas.Label((12, 45), bg=DEEPBLUE, radius={'border_radius': 6}, midbottom=(18, 58))
bar_led.join(arm_head)
pl_bg_kf = fantas.LabelKeyFrame(point_led, 'bg', LIGHTGREEN, 10, u.curve)
bl_bg_kf = fantas.LabelKeyFrame(bar_led, 'bg', LIGHTGREEN, 10, u.curve)

def rotate_record():
    if record_angle_kf not in u.keyframe_queue:
        u.keyframe_queue.append(record_angle_kf)
    arm_angle_kf.value = 10
    arm_angle_kf.totalframe = 20
    arm_angle_kf.launch('continue')
    arm_pos_kf.value = (300, 0)
    arm_pos_kf.totalframe = 20
    arm_pos_kf.launch('continue')
    pl_bg_kf.value = bl_bg_kf.value = LIGHTGREEN
    pl_bg_kf.launch('continue')
    bl_bg_kf.launch('continue')

def stop_record():
    arm_angle_kf.value = 30
    arm_angle_kf.totalframe = 10
    arm_angle_kf.launch('continue')
    arm_pos_kf.value = (370, -10)
    arm_pos_kf.totalframe = 10
    arm_pos_kf.launch('continue')
    pl_bg_kf.value = bl_bg_kf.value = DEEPBLUE
    pl_bg_kf.launch('continue')
    bl_bg_kf.launch('continue')
    record_angle_kf.stop()
record_angle_kf.bind_endupwith(record_angle_kf.launch, 'recover', 0)


class PlayButtonMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)

    def mousein(self):
        if self.mousedown is None:
            self.ui.larger()
        else:
            self.ui.smaller()

    def mouseout(self):
        self.ui.smaller()

    def mousepress(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.smaller()

    def mouserelease(self, pos, button):
        if not self.mouseon:
            self.ui.smaller()
        else:
            self.ui.larger()

    def mouseclick(self):
        if self.ui.played:
            self.ui.pause()
            my_serial.send_write_order([0x07])
        else:
            self.ui.play()
            my_serial.send_write_order([0x06])
            my_serial.send_read_order([0x07], update_music_info)
        u.sounds['play'].play()

class PlayButton(fantas.IconText):
    play_text = chr(0xe60c)
    pause_text = chr(0xe693)
    osize_p = 48
    osize_np = 42
    lsize_p = 60
    lsize_np = 54
    istyle = get_text(osize_np, DARKGRAY)

    def __init__(self, **kwargs):
        super().__init__(self.play_text, u.fonts['iconfont'], self.istyle, **kwargs)
        self.size_kf = fantas.TextKeyFrame(self, 'size', self.osize_np, 10, u.harmonic_curve)

        self.mousewidget = PlayButtonMouseWidget(self)
        self.mousewidget.apply_event()

        self.played = False

    def larger(self):
        if self.played:
            self.size_kf.value = self.lsize_p
        else:
            self.size_kf.value = self.lsize_np
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')

    def smaller(self):
        if self.played:
            self.size_kf.value = self.osize_p
        else:
            self.size_kf.value = self.osize_np
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')

    def play(self):
        self.text = self.pause_text
        self.played = True
        self.update_img()
        if not stop_button.played:
            stop_button.play()
        rotate_record()

    def pause(self):
        self.text = self.play_text
        self.played = False
        self.update_img()
        stop_record()


class StopButtonMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 1)

    def mousepress(self, pos, button):
        if button == self.mousedown == 1 and self.ui.played:
            my_serial.send_write_order([0x08])
            my_serial.send_read_order([0x07], update_music_info)
            # self.ui.unplay()
            u.sounds['stop'].play()

class StopButton(fantas.Label):
    osize = (40, 40)
    lsize = (48, 48)
    oradius = 4
    lradius = 10
    obg = DARKGRAY
    lbg = LIGHTRED

    def __init__(self, **anchor):
        super().__init__(self.osize, bg=self.obg, radius={'border_radius': self.oradius}, **anchor)
        self.size_kf = fantas.LabelKeyFrame(self, 'size', self.osize, 10, u.harmonic_curve)
        self.radius_kf = fantas.LabelKeyFrame(self, 'radius', self.oradius, 10, u.harmonic_curve)
        self.bg_kf = fantas.LabelKeyFrame(self, 'bg', self.obg, 10, u.harmonic_curve)

        self.mousewidget = StopButtonMouseWidget(self)
        self.mousewidget.apply_event()

        self.played = False

    def larger(self):
        self.size_kf.value = self.lsize
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')
        self.radius_kf.value = self.lradius
        self.radius_kf.totalframe = 10
        self.radius_kf.launch('continue')
        self.bg_kf.value = self.lbg
        self.bg_kf.totalframe = 10
        self.bg_kf.launch('continue')

    def smaller(self):
        self.size_kf.value = self.osize
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')
        self.radius_kf.value = self.oradius
        self.radius_kf.totalframe = 6
        self.radius_kf.launch('continue')
        self.bg_kf.value = self.obg
        self.bg_kf.totalframe = 6
        self.bg_kf.launch('continue')

    def play(self):
        self.played = True
        self.larger()

    def unplay(self):
        self.played = False
        self.smaller()
        if play_button.played:
            play_button.pause()


class NextButtonMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)

    def mousein(self):
        if self.mousedown is None:
            self.ui.larger()
        else:
            self.ui.smaller()

    def mouseout(self):
        self.ui.smaller()

    def mousepress(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.smaller()

    def mouserelease(self, pos, button):
        if not self.mouseon:
            self.ui.smaller()
        else:
            self.ui.larger()

    def mouseclick(self):
        if music_total_index != 0:
            self.ui.next_ani()
            my_serial.send_write_order([0x0b, music_total_index - 1])
            my_serial.send_read_order([0x07], update_music_info)
            my_serial.send_write_order([0x0e])
            u.sounds['next'].play()

class NextButton(fantas.IconText):
    itext = chr(0xe815)
    osize = 60
    lsize = 72
    istyle = get_text(osize, DARKGRAY)
    posx_offset = 60

    def __init__(self, **kwargs):
        super().__init__(self.itext, u.fonts['iconfont'], self.istyle, **kwargs)
        self.oposx = self.rect.center[0]
        self.size_kf = fantas.TextKeyFrame(self, 'size', self.osize, 10, u.harmonic_curve)
        self.alpha_kf = fantas.UiKeyFrame(self, 'alpha', 0, 15, u.faster_curve)
        self.alpha_kf_trigger = fantas.Trigger(self.alpha_kf.launch, 'continue')
        self.pos_kf = fantas.RectKeyFrame(self, 'centerx', self.oposx, 20, u.faster_curve)

        self.mousewidget = NextButtonMouseWidget(self)
        self.mousewidget.apply_event()

    def larger(self):
        self.size_kf.value = self.lsize
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')

    def smaller(self):
        self.size_kf.value = self.osize
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')

    def next_ani(self):
        self.alpha_kf.value = 0
        self.alpha_kf.curve = u.faster_curve
        self.alpha_kf.bind_endupwith(self.ani1)
        self.alpha_kf.launch('continue')
        self.pos_kf.value = self.oposx + self.posx_offset
        self.pos_kf.curve = u.faster_curve
        self.pos_kf.bind_endupwith(self.ani2)
        self.pos_kf.launch('continue')
        if play_button.played:
            play_button.pause()

    def ani1(self):
        self.alpha_kf.value = 255
        self.alpha_kf.curve = u.slower_curve
        self.alpha_kf.bind_endupwith(None)
        self.alpha_kf_trigger.launch(10)

    def ani2(self):
        self.rect.centerx = self.oposx - self.posx_offset
        self.pos_kf.value = self.oposx
        self.pos_kf.curve = u.slower_curve
        self.pos_kf.bind_endupwith(self.next)
        self.pos_kf.launch('continue')

    def next(self):
        if music_total_index == 0:
            return
        play_button.play()


class SpeedButtonMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)

    def mousein(self):
        if self.mousedown is None:
            self.ui.larger()
        else:
            self.ui.smaller()

    def mouseout(self):
        self.ui.smaller()

    def mousepress(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.smaller()

    def mouserelease(self, pos, button):
        if not self.mouseon:
            self.ui.smaller()
        else:
            self.ui.larger()

    def mouseclick(self):
        self.ui.change_speed()
        u.sounds['speed'].play()

class SpeedButton(fantas.IconText):
    itext = chr(0xe61a)
    osize = 48
    lsize = 60
    stosize = 12
    stlsize = 14
    stopos = (26, 44)
    stlpos = (32, 54)
    istyle = get_text(osize, DARKGRAY)
    tstyle = get_text(stosize, DARKGRAY)
    tstyle['style'] = pygame.freetype.STYLE_STRONG
    speed_texts = ('0.5x', '1.0x', '2.0x')

    def __init__(self, **kwargs):
        super().__init__(self.itext, u.fonts['iconfont'], self.istyle, **kwargs)
        self.speed = 1
        self.speed_text = fantas.Text(self.speed_texts[self.speed], u.fonts['deyi'], self.tstyle, midbottom=self.stopos)
        self.speed_text.join(self)

        self.size_kf = fantas.TextKeyFrame(self, 'size', 0, 10, u.harmonic_curve)
        self.st_size_kf = fantas.TextKeyFrame(self.speed_text, 'size', 0, 10, u.harmonic_curve)
        self.st_pos_kf = fantas.RectKeyFrame(self.speed_text, 'midbottom', self.stopos, 10, u.harmonic_curve)

        self.mousewidget = SpeedButtonMouseWidget(self)
        self.mousewidget.apply_event()

    def larger(self):
        self.size_kf.value = self.lsize
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')
        self.st_size_kf.value = self.stlsize
        self.st_size_kf.totalframe = 10
        self.st_size_kf.launch('continue')
        self.st_pos_kf.value = self.stlpos
        self.st_pos_kf.totalframe = 10
        self.st_pos_kf.launch('continue')

    def smaller(self):
        self.size_kf.value = self.osize
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')
        self.st_size_kf.value = self.stosize
        self.st_size_kf.totalframe = 6
        self.st_size_kf.launch('continue')
        self.st_pos_kf.value = self.stopos
        self.st_pos_kf.totalframe = 6
        self.st_pos_kf.launch('continue')
    
    def set_speed(self, speed):
        self.speed = speed
        my_serial.send_write_order([0x09, self.speed])
        self.speed_text.text = self.speed_texts[self.speed]
        self.speed_text.update_img()
        if self.speed == 2:
            record_angle_kf.currentframe = round(180 * (record_angle_kf.currentframe / record_angle_kf.totalframe))
            record_angle_kf.totalframe = 180
        elif self.speed == 1:
            record_angle_kf.currentframe = round(360 * (record_angle_kf.currentframe / record_angle_kf.totalframe))
            record_angle_kf.totalframe = 360
        else:
            record_angle_kf.currentframe = round(720 * (record_angle_kf.currentframe / record_angle_kf.totalframe))
            record_angle_kf.totalframe = 720

    def change_speed(self):
        self.set_speed((self.speed + 1) % 3)


class ModeButtonMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)

    def mousein(self):
        if self.mousedown is None:
            self.ui.larger()
        else:
            self.ui.smaller()

    def mouseout(self):
        self.ui.smaller()

    def mousepress(self, pos, button):
        if button == self.mousedown == 1:
            self.ui.smaller()

    def mouserelease(self, pos, button):
        if not self.mouseon:
            self.ui.smaller()
        else:
            self.ui.larger()

    def mouseclick(self):
        self.ui.change_mode()
        u.sounds['mode'].play()

class ModeButton(fantas.IconText):
    itexts = (chr(0xe6a6), chr(0xe60d), chr(0xe60b), chr(0xe6db), chr(0xe622))
    osize = 48
    lsize = 60
    istyle = get_text(osize, DARKGRAY)

    def __init__(self, **kwargs):
        self.mode = 0
        super().__init__(self.itexts[self.mode], u.fonts['iconfont'], self.istyle, **kwargs)
        self.size_kf = fantas.TextKeyFrame(self, 'size', self.osize, 10, u.harmonic_curve)

        self.mousewidget = ModeButtonMouseWidget(self)
        self.mousewidget.apply_event()

    def larger(self):
        self.size_kf.value = self.lsize
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')

    def smaller(self):
        self.size_kf.value = self.osize
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')
    
    def set_mode(self, mode):
        self.mode = mode
        my_serial.send_write_order([0x0a, self.mode])
        self.text = self.itexts[self.mode]
        self.update_img()

    def change_mode(self):
        self.set_mode((self.mode + 1) % 5)


class ProcessBarMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
        self.start = None
        self.pos = None

    def mousepress(self, pos, button):
        if button == self.mousedown == 1 and play_button.played:
            self.ui.larger()
            self.start = self.ui.bar.size[0]
            self.pos = pos[0]
            play_button.pause()
            my_serial.send_write_order([0x07])

    def mouserelease(self, pos, button):
        self.ui.smaller()
        if self.pos is not None:
            self.pos = None

    def mousemove(self, pos):
        if self.pos is not None:
            self.ui.set_bar_size(self.start + pos[0] - self.pos)

class ProcessBar(fantas.Label):
    oheight = 12
    lheight = 16
    osize = (240, oheight)
    lsize = (260, lheight)

    def __init__(self, **anchor):
        super().__init__(self.osize, bg=DARKGRAY, radius={'border_radius': 48}, **anchor)
        self.size_kf = fantas.UiKeyFrame(self, 'size', self.osize, 10, u.slower_curve)
        self.height = self.oheight
        self.bar = fantas.Label((self.oheight, self.oheight), bg=WHITE, radius={'border_radius': 48}, topleft=(0, 0))
        self.bar.join(self)
        self.bar.anchor = 'topleft'
        self.bar_size_kf = fantas.LabelKeyFrame(self.bar, 'size', (self.oheight, self.oheight), 10, u.slower_curve)

        self.mousewidget = ProcessBarMouseWidget(self)
        # self.mousewidget.apply_event()

    def larger(self):
        self.bar_size_kf.value = (self.bar_size_kf.value[0], self.oheight)
        self.bar_size_kf.totalframe = 10
        self.bar_size_kf.launch('continue')
        self.size_kf.value = self.lsize
        self.size_kf.totalframe = 10
        self.size_kf.launch('continue')

    def smaller(self):
        self.bar_size_kf.value = (self.bar_size_kf.value[0], self.oheight)
        self.bar_size_kf.totalframe = 6
        self.bar_size_kf.launch('continue')
        self.size_kf.value = self.osize
        self.size_kf.totalframe = 6
        self.size_kf.launch('continue')

    def set_bar_size(self, size):
        size = max(min(size, self.osize[0]), self.oheight)
        self.bar_size_kf.value = (size, self.oheight)
        self.bar_size_kf.totalframe = 6
        self.bar_size_kf.launch('continue')
    
    def set_process(self, r):
        self.set_bar_size(round(r * self.osize[0]))

speed_button = SpeedButton(center=(300, 240))
speed_button.join(board)
stop_button = StopButton(center=(360, 240))
stop_button.join(board)
play_button = PlayButton(center=(420, 240))
play_button.join(board)
next_button = NextButton(center=(480, 240))
next_button.join(board)
mode_button = ModeButton(center=(540, 240))
mode_button.join(board)

process_bar = ProcessBar(center=(420, 288))
process_bar.join(board)

music_name = fantas.Text('* ---- *', u.fonts['deyi'], music_name_style, center=(420, 120))
music_name.join(board)
music_total_index = 0
music_total_tick = 0

def update_music_info(data):
    global music_total_index, music_total_tick
    if data[0] == 0:
        music_total_index = 0
        music_total_tick = 0
        music_name.text = '* ---- *'
        music_name.update_img()
        if stop_button.played:
            stop_button.unplay()
        return
    s = ''
    for i in range(len(data)):
        if data[i] == 0:
            break
        s += chr(data[i])
    music_name.text = s
    music_name.update_img()
    music_total_tick = data[i + 1] << 24 | data[i + 2] << 16 | data[i + 3] << 8 | data[i + 4]
    music_total_index = data[i + 5]

def sync_play_info(data):
    if data[0] == 0 and stop_button.played:
        stop_button.unplay()
    elif data[0] == 1 and not play_button.played:
        play_button.play()
    elif data[0] == 2 and play_button.played:
        play_button.pause()
    if data[1] != speed_button.speed:
        speed_button.set_speed(data[1])
    if data[2] != mode_button.mode:
        mode_button.set_mode(data[2])
    if music_total_index == 0:
        return
    process_bar.set_process(data[3] / music_total_index)
    if music_total_index - data[3] < 3 or data[3] < 3:
        my_serial.send_read_order([0x07], update_music_info)
info_syncer = sync.SyncTrigger('play_info', sync_play_info)
