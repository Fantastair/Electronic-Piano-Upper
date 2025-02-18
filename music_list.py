import pygame
import fantas
from fantas import uimanager as u
import my_serial
from style import *

board = fantas.fantas.Label((u.WIDTH - 216, u.HEIGHT // 2 - 80))

enter_button = fantas.SmoothColorButton((320, 80), ml_button_color, 0, radius={'border_radius': 24}, center=(u.WIDTH // 2 - 113, u.HEIGHT // 4 - 40))
enter_button.join(board)
fantas.Text('查看音乐列表', u.fonts['deyi'], ml_button_text_style, center=(160, 40)).join(enter_button)

root_temp = None

def go():
    global root_temp
    root_temp = u.root
    u.root = root
    refresh_data()
enter_button.bind(go)

def back():
    u.root = root_temp

root = fantas.Root(FAKEWHITE)

up_bar = fantas.Label((u.WIDTH, 80), bg=LIGHTGRAY, topleft=(0, 0))
up_bar.join(root)

fantas.Text('音频数据列表', u.fonts['deyi'], mlub_tip_text_style, center=(u.WIDTH // 2, 40)).join(up_bar)

back_button = fantas.SmoothColorButton((128, 40), mlub_button_color, 2, radius={'border_radius': 8}, center=(128, 40))
back_button.join(up_bar)
back_button.bind(back)
fantas.Text('<< 返回', u.fonts['deyi'], mlub_button_text_style, center=(64, 20)).join(back_button)

def refresh_data():
    global ba_filename, ba_data, ba_state
    ba_data = {}
    ba_state = 0
    my_serial.send_read_order([0x04], recv_backup_data)
    music_list_box.rect.topleft = (0, 100)
    scroll_bar.rect.topright = (u.WIDTH, 80)

refresh_button = fantas.SmoothColorButton((128, 40), mlub_button_color, 2, radius={'border_radius': 8}, center=(u.WIDTH - 128, 40))
refresh_button.join(up_bar)
refresh_button.bind(refresh_data)
fantas.Text('刷新', u.fonts['deyi'], mlub_button_text_style, center=(64, 20)).join(refresh_button)

ba_data = {}
ba_state = 0    # 0：接收总音频数；1：接收数据包数；2：接收音频名称；3：接收音符轨道；4：接收时刻轨道
ba_temp1 = 0    # 总音频数
ba_temp2 = 0    # 音符数据包数
ba_temp3 = ''   # 音频名称
ba_temp4 = 0    # 时刻数据包数
ba_temp5 = 0    # 已接受音频数

def recv_backup_data(data):
    global ba_data, ba_state, ba_temp1, ba_temp2, ba_temp3, ba_temp4, ba_temp5

    if ba_state == 3:
        for i in range(0, len(data), 2):
            ba_data[ba_temp3][0].append(data[i] + data[i + 1] * 256)
        ba_temp2 -= 1
        if ba_temp2 == 0:
            ba_state = 4
        my_serial.send_read_order([0x04], recv_backup_data)
    elif ba_state == 4:
        for i in range(0, len(data), 2):
            ba_data[ba_temp3][1].append(data[i] + data[i + 1] * 256)
        ba_temp4 -= 1
        if ba_temp4 == 0:
            ba_temp5 += 1
            ba_state = 1
        my_serial.send_read_order([0x04], recv_backup_data)
    elif ba_state == 2:
        ba_temp3 = ''
        for i in data:
            if i != 0:
                ba_temp3 += chr(i)
            else:
                break
        ba_data[ba_temp3] = [[], []]
        ba_state = 3
        my_serial.send_read_order([0x04], recv_backup_data)
    elif ba_state == 1 and len(data) == 1:
        if data[0] == 0:    # 发送一个数据 0，表示结束备份
            ba_state = 0
            create_list(ba_data)
        else:
            ba_temp2 = ba_temp4 = data[0]
            ba_state = 2
            my_serial.send_read_order([0x04], recv_backup_data)
    elif ba_state == 0 and len(data) == 1:
        ba_temp1 = data[0]
        ba_state = 1
        my_serial.send_read_order([0x04], recv_backup_data)
    else:
        ba_state = 0

def create_list(data):
    global music_item_list
    while music_item_list:
        music_item_list.pop().leave()
    for name in data:
        music_item_list.append(MusicItem(name, data[name], midtop=(u.WIDTH // 2, 0)))
        music_item_list[-1].join(music_list_box)
    adjust_list()

def adjust_list():
    top_temp = 0
    for i in music_item_list:
        i.move_top(top_temp)
        top_temp += i.size_kf.value[1] + 20
    mlb_size_kf.value = (u.WIDTH, top_temp)
    mlb_size_kf.launch('continue')
    scroll_bar.set_size((10, (u.HEIGHT - 100) ** 2 / mlb_size_kf.value[1]))

class MusicItemMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
    
    def mouseclick(self):
        if self.mousedown != fantas.LEFTMOUSEBUTTON or self.ui.rect.top + self.ui.father.rect.top < 80 or pygame.mouse.get_pos()[1] > self.ui.rect.top + self.ui.father.rect.top + 120:
            return
        if self.ui.detail_showed:
            self.ui.hide_detail()
        else:
            self.ui.show_detail()

class MusicItemScrollBarMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)
        self.pressed_pos = None
        self.start_pos = None

    def mousepress(self, pos, button):
        if self.mousedown == button == fantas.LEFTMOUSEBUTTON:
            self.pressed_pos = pos[0]
            self.start_pos = self.ui.rect.left
    
    def mouserelease(self, pos, button):
        if self.pressed_pos is not None:
            self.pressed_pos = None
    
    def mousemove(self, pos):
        if self.pressed_pos is not None:
            self.ui.father.father.move_scroll_bar(self.start_pos + pos[0] - self.pressed_pos)

class MusicItem(fantas.Label):
    normal_size = (u.WIDTH - 40, 120)
    detail_size = (u.WIDTH - 40, u.HEIGHT - 120)
    normal_bd = 2
    detail_bd = 6
    normal_radius = 24
    detail_radius = 48
    name_text_style = get_text(48, DEEPBLUE)
    time_text_style = get_text(36, DEEPBLUE)
    note_text_style = get_text(36, DEEPBLUE)
    tick_text_style = get_text(16, LIGHTGRAY)

    def __init__(self, name, data, **anchor):
        super().__init__(self.normal_size, self.normal_bd, LIGHTGRAY, DEEPBLUE, {'border_radius': self.normal_radius}, **anchor)
        self.anchor = 'midtop'
        self.name = name
        self.note_data = data[0]
        self.tick_data = data[1]
        self.name_text = fantas.Text(name, u.fonts['deyi'], self.name_text_style, midleft=(40, 60))
        self.name_text.join(self)
        self.name_text.anchor = 'midleft'
        self.time_text = fantas.Text(str(self.get_total_time()) + ' s', u.fonts['deyi'], self.time_text_style, midright=(self.normal_size[0] - 40, 60))
        self.time_text.join(self)
        self.time_text.anchor = 'midright'
        self.pos_kf = fantas.RectKeyFrame(self, 'top', 0, 16, u.harmonic_curve)
        self.size_kf = fantas.LabelKeyFrame(self, 'size', self.normal_size, 18, u.harmonic_curve)
        self.radius_kf = fantas.LabelKeyFrame(self, 'radius', self.detail_radius, 18, u.harmonic_curve)
        self.bd_kf = fantas.LabelKeyFrame(self, 'bd', self.detail_bd, 18, u.harmonic_curve)
        self.detail_showed = False
        self.mousewidget = MusicItemMouseWidget(self)
        self.mousewidget.apply_event()
        self.data_box = fantas.Label((self.detail_size[0] - 120, self.detail_size[1] - 260), bg=FAKEWHITE, radius={'border_radius': 42}, center=(self.detail_size[0] // 2 + 20, self.detail_size[1] // 2 + 70))
        self.data_box.join(self)
        lh = self.detail_size[1] // 10 - 26
        for i in range(8):
            fantas.Text(str((7 - i) % 7 + 1), u.fonts['deyi'], self.note_text_style, center=(60, 265 + i * lh)).join(self)
        fantas.CircleLabel(3, DEEPBLUE, center=(62, 242)).join(self)
        for i in range(9):
            fantas.Label((self.detail_size[0] - 120, 2), bg=DARKGRAY, topleft=(0, (i + 1) * lh)).join(self.data_box)
        self.note_box = fantas.Label((0, self.detail_size[1] - 260))
        self.note_box.anchor = 'topleft'
        self.note_box.join(self.data_box)
        note_temp = [None] * 8
        left_temp = 0
        for i in range(len(self.note_data)):
            left_temp += self.tick_data[i] * 2
            if self.note_data[i] < 8:
                note_temp[(7 - self.note_data[i])] = fantas.Label((0, lh), bg=DEEPGREEN, topleft=(left_temp, ((7 - self.note_data[i]) + 1) * lh))
                note_temp[(7 - self.note_data[i])].anchor = 'midleft'
                note_temp[(7 - self.note_data[i])].join(self.note_box)
            else:
                note_temp[15 - self.note_data[i]].set_size((left_temp - note_temp[15 - self.note_data[i]].rect.left, lh))
                note_temp[15 - self.note_data[i]] = None
        self.note_box.set_size((left_temp, self.detail_size[1] - 260))
        for i in range(0, left_temp, 16):
            fantas.Label((1, 8), bg=LIGHTGRAY, midbottom=(i, self.detail_size[1] - 260)).join(self.note_box)
        for i in range(0, left_temp, 64):
            fantas.Label((2, 16), bg=LIGHTGRAY, midbottom=(i, self.detail_size[1] - 260)).join(self.note_box)
        for i in range(0, left_temp, 128):
            fantas.Label((3, 24), bg=LIGHTGRAY, midbottom=(i, self.detail_size[1] - 260)).join(self.note_box)
            fantas.Text(str(i / 256), u.fonts['deyi'], self.tick_text_style, midbottom=(i, self.detail_size[1] - 283)).join(self.note_box)
        if left_temp > self.detail_size[0] - 120:
            self.scroll_bar = fantas.Label(((self.detail_size[0] - 120) ** 2 / left_temp, 10), bg=LIGHTGRAY, topleft=(0, 0))
            self.scroll_bar.join(self.data_box)
            self.sb_mousewidget = MusicItemScrollBarMouseWidget(self.scroll_bar)
            self.sb_mousewidget.apply_event()

    def move_scroll_bar(self, left):
        if left < 0:
            left = 0
        elif left > self.detail_size[0] - 120 - self.scroll_bar.size[0]:
            left = self.detail_size[0] - 120 - self.scroll_bar.size[0]
        self.scroll_bar.rect.left = left
        self.scroll_bar.mark_update()
        self.note_box.rect.left = -(self.note_box.size[0] - self.detail_size[0] + 120) * left / (self.detail_size[0] - 120 - self.scroll_bar.size[0])

    def get_total_ticks(self):
        return sum(self.tick_data)

    def get_total_time(self):
        return round(self.get_total_ticks() / 128, 1)

    def move_top(self, top):
        self.pos_kf.value = top
        self.pos_kf.launch('continue')

    def show_detail(self):
        if not self.detail_showed:
            self.size_kf.value = self.detail_size
            self.size_kf.totalframe = 18
            mlb_size_kf.totalframe = 6
            self.size_kf.launch('continue')
            self.radius_kf.value = self.detail_radius
            self.radius_kf.launch('continue')
            self.bd_kf.value = self.detail_bd
            self.bd_kf.launch('continue')
            self.detail_showed = True
            adjust_list()
            self.show_self_at_top()

    def hide_detail(self):
        if self.detail_showed:
            self.size_kf.value = self.normal_size
            self.size_kf.totalframe = 10
            mlb_size_kf.totalframe = 24
            self.size_kf.launch('continue')
            self.radius_kf.value = self.normal_radius
            self.radius_kf.launch('continue')
            self.bd_kf.value = self.normal_bd
            self.bd_kf.launch('continue')
            self.detail_showed = False
            adjust_list()
            self.show_self_at_top()
    
    def show_self_at_top(self):
        t = 0
        for i in music_item_list:
            if i == self:
                break
            t += i.size_kf.value[1] + 20
        mlb_pos_kf.value = 100 - t
        mlb_pos_kf.launch('continue')

class MusicListBoxMouseWidget(fantas.MouseBase):
    def __init__(self):
        super().__init__(music_list_box, 3)
        self.apply_event()

    def mousescroll(self, x, y):
        mlb_pos_kf.value += y * 60
        if mlb_pos_kf.value > 100:
            mlb_pos_kf.value = 100
        elif mlb_pos_kf.value < u.HEIGHT - music_list_box.size[1]:
            mlb_pos_kf.value = u.HEIGHT - music_list_box.size[1]
        mlb_pos_kf.launch('continue')
        sb_pos_kf.value = round(80 + (u.HEIGHT - 80 - scroll_bar.size[1]) * (mlb_pos_kf.value - 100) / (u.HEIGHT - music_list_box.size[1] - 100))
        sb_pos_kf.launch('continue')

music_item_list = []
music_list_box = fantas.Label((u.WIDTH, 0), topleft=(0, 100))
music_list_box.anchor = 'topleft'
music_list_box.join_to(root, 0)
mlb_size_kf = fantas.LabelKeyFrame(music_list_box, 'size', (u.WIDTH, 0), 6, u.curve)
mlb_pos_kf = fantas.RectKeyFrame(music_list_box, 'top', 100, 12, u.harmonic_curve)
MusicListBoxMouseWidget()

scroll_bar = fantas.Label((10, 0), bg=LIGHTGRAY, topright=(u.WIDTH, 80))
scroll_bar.anchor = 'topright'
scroll_bar.join_to(root, 0)
sb_pos_kf = fantas.RectKeyFrame(scroll_bar, 'top', 100, 12, u.harmonic_curve)
