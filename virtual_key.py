import fantas
from fantas import uimanager as u
import my_serial

from style import *

class VirtualKey(fantas.Label):
    def  __init__(self, text, info, num, **anchor):
        global itl_height
        super().__init__((64, 64), 4, LIGHTGRAY, DARKGRAY, {'border_radius': 8}, **anchor)
        self.num = num
        self.pins = [
            fantas.Label((4, 8), bg=LIGHTGRAY, radius={'border_top_left_radius': 2, 'border_top_right_radius': 2}, midbottom=(16 + self.rect.left, 0 + self.rect.top)),
            fantas.Label((4, 8), bg=LIGHTGRAY, radius={'border_top_left_radius': 2, 'border_top_right_radius': 2}, midbottom=(48 + self.rect.left, 0 + self.rect.top)),
            fantas.Label((4, 8), bg=LIGHTGRAY, radius={'border_bottom_left_radius': 2, 'border_bottom_right_radius': 2}, midtop=(16 + self.rect.left, 64 + self.rect.top)),
            fantas.Label((4, 8), bg=LIGHTGRAY, radius={'border_bottom_left_radius': 2, 'border_bottom_right_radius': 2}, midtop=(48 + self.rect.left, 64 + self.rect.top)),
        ]
        fantas.CircleLabel(2, DARKGRAY, center=(8, 8)).join(self)
        fantas.CircleLabel(2, DARKGRAY, center=(56, 8)).join(self)
        fantas.CircleLabel(2, DARKGRAY, center=(56, 56)).join(self)
        fantas.CircleLabel(2, DARKGRAY, center=(8, 56)).join(self)
        self.button = fantas.CircleLabel(16, DEEPBLUE, center=(32, 32))
        self.button.join(self)
        self.text = fantas.Text(text, u.fonts['shuhei'], virtual_button_text_style, center=(16, 15))
        self.text.join(self.button)
        self.mousewidget = VirtualKeyMouseWidget(self)
        self.mousewidget.apply_event()
        self.visual_pos = -itl_height
        self.info = fantas.Text(info, u.fonts['shuhei'], dict(vb_info_text_style), center=(120, itl_height + 30))
        self.info_size_kf = fantas.TextKeyFrame(self.info, 'size', 40, 8, u.slower_curve)
        self.info_color_kf = fantas.TextKeyFrame(self.info, 'fgcolor', DARKRED, 8, u.slower_curve)
        itl_height += 60
        info_text_label.set_size((240, itl_height))
        self.info.join(info_text_label)
        self.pushed = False

    def join(self, node):
        for i in self.pins:
            i.join(node)
        super().join(node)
    
    def release(self, from_sync=False):
        self.pushed = False
        u.sounds['virtual_button'].play()
        if not from_sync:
            my_serial.send_write_order([0x00, 0x01, self.num])
        self.info_size_kf.value = 28
        self.info_color_kf.value = DEEPBLUE
        self.info_size_kf.launch('continue')
        self.info_color_kf.launch('continue')
    
    def push(self, from_sync=False):
        self.pushed = True
        u.sounds['virtual_button'].play()
        if not from_sync:
            my_serial.send_write_order([0x00, 0x00, self.num])
        self.info_size_kf.value = 40
        self.info_color_kf.value = DARKRED
        self.info_size_kf.launch('continue')
        self.info_color_kf.launch('continue')

class VirtualKeyMouseWidget(fantas.MouseBase):
    def __init__(self, ui):
        super().__init__(ui, 2)

    def mousepress(self, pos, button):
        if self.mousedown == button == fantas.LEFTMOUSEBUTTON:
            if self.mouseon:
                self.ui.push()
    
    def mousein(self):
        show_info(self.ui)
    
    def mouseout(self):
        show_info()

    def mouserelease(self, pos, button):
        if button == fantas.LEFTMOUSEBUTTON:
            if self.ui.pushed:
                self.ui.release()

info_box = fantas.Label((240, 60), 4, LIGHTGRAY, DEEPBLUE, {'border_radius': 16}, center=(267, 140))

info_text_label = fantas.Label((240, 0), topleft=(0, 60))
info_text_label.anchor = 'topleft'
info_text_label.join(info_box)
itl_pos_kf = fantas.RectKeyFrame(info_text_label, 'top', 0, 15, u.slower_curve)

itl_height = 0

def show_info(key: VirtualKey = None):
    if key is None:
        itl_pos_kf.value = 60
    else:
        itl_pos_kf.value = key.visual_pos
    itl_pos_kf.launch('continue')
