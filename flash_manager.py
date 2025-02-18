import pickle
from pathlib import Path
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pygame
import fantas
from fantas import uimanager as u
import my_serial

from style import *


board = fantas.fantas.Label((u.WIDTH - 216, u.HEIGHT // 2 - 80))

tip_text = fantas.Text('存储管理器', u.fonts['shuhei'], memory_text_style, center=(u.WIDTH // 2 - 113, 40))
tip_text.join(board)
tip_text_alpha_kf = fantas.UiKeyFrame(tip_text, 'alpha', 0, 15, u.harmonic_curve)

def set_tip_text1(text):
    tip_text_alpha_kf.totalframe = 12
    tip_text_alpha_kf.value = 0
    tip_text_alpha_kf.bind_endupwith(set_tip_text2, text)
    tip_text_alpha_kf.launch('continue')

def set_tip_text2(text):
    tip_text.text = text
    tip_text.style['size'] = 30
    tip_text.update_img()
    tip_text_alpha_kf.totalframe = 8
    tip_text_alpha_kf.value = 255
    tip_text_alpha_kf.bind_endupwith(None)
    tip_text_alpha_kf.launch('continue')

def reset_tip_text1():
    tip_text_alpha_kf.totalframe = 12
    tip_text_alpha_kf.value = 0
    tip_text_alpha_kf.bind_endupwith(reset_tip_text2)
    tip_text_alpha_kf.launch('continue')

def reset_tip_text2():
    tip_text.text = '存储管理器'
    tip_text.style['size'] = 42
    tip_text.update_img()
    tip_text_alpha_kf.totalframe = 8
    tip_text_alpha_kf.value = 255
    tip_text_alpha_kf.bind_endupwith(None)
    tip_text_alpha_kf.launch('continue')


class MemoryButtonMouseWidget(fantas.ColorButtonMouseWidget):
    def mousein(self):
        super().mousein()
        set_tip_text1(self.ui.tip_text)
    
    def mouseout(self):
        super().mouseout()
        reset_tip_text1()

class MemoryButton(fantas.SmoothColorButton):
    height = 40
    tstyle = get_text(24, DEEPBLUE)

    def __init__(self, width, text, tip_text, colors=memory_button_color, mousewidget=MemoryButtonMouseWidget, **anchor):
        super().__init__((width, self.height), colors, 2, mousewidget, radius={'border_radius': 8}, **anchor)
        self.text = fantas.Text(text, u.fonts['shuhei'], self.tstyle, center=(width // 2, self.height // 2 - 1))
        self.text.join(self)
        self.tip_text = tip_text


flash_table = []
flash_table_data = []
data_length = 0
ex_filename = None
export_table_button = MemoryButton(120, '导出表头', '将表头数据导出为文件', center=(80, 120))
export_table_button.join(board)
end_func = None
def record_table(data):
    global flash_table, flash_table_data, data_length
    flash_table_data += data
    if data[0] == 2:
        s = ''
        for i in range(1, 15):
            if data[i] != 0:
                s += chr(data[i])
            else:
                break
        flash_table.append((s, data_length))
    data_length += 1
    if data_length == 64:
        process_bar.set_process(10 + round(data_length / 64 * 80, 2), end_func)
    else:
        process_bar.set_process(10 + round(data_length / 64 * 80, 2))

def save_table():
    global ex_filename, end_func
    if ex_filename:
        with Path(ex_filename).open('wb') as f:
            f.write(bytes(flash_table_data))
        ex_filename = None
        process_bar.set_process(100)
    else:
        process_bar.set_process(0)
    end_func = None

def update_table():
    global flash_table, flash_table_data, data_length
    flash_table = []
    flash_table_data = []
    data_length = 0
    for i in range(64):
        my_serial.send_read_order([0x03, i], record_table)


def export_table():
    global ex_filename, end_func
    ex_filename = asksaveasfilename(defaultextension='.ftd', filetypes=[('Flash Table Data', '*.ftd')], initialfile='flash_table_data.ftd', title='导出表头数据', initialdir='./')
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (720, 110)}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (720, 110)}))
    if ex_filename:
        process_bar.set_process(10)
        end_func = save_table
        update_table()

import_table_button = MemoryButton(120, '导入表头', '从文件将表头数据写入到下位机', center=(240, 120))
import_table_button.join(board)
def import_table():
    im_filename = askopenfilename(filetypes=[('Flash Table Data', '*.ftd')], title='导入表头数据', initialdir='./')
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (720, 110)}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (720, 110)}))
    process_bar.set_process(10)
    if im_filename:
        with Path(im_filename).open('rb') as f:
            data = f.read(1024)
        im_filename = None
        process_bar.set_process(20)
        my_serial.send_write_order([0x03, 63])
        process_bar.set_process(30)
        for i in range(0, 1024, 16):
            my_serial.send_write_order([0x02, i // 16] + list(data[i: i + 16]))
            process_bar.set_process(30 + 70 * (i + 16) // 1024)
    else:
        process_bar.set_process(0)

clear_memory_button = MemoryButton(220, '清除用户存储数据', '清除存储的音频', center=(450, 120))
clear_memory_button.join(board)
def clear_memory():
    global end_func
    end_func = clear_memory_
    update_table()
clear_memory_button.bind(clear_memory)

def clear_memory_():
    global end_func
    process_bar.set_process(0)
    for i in flash_table:
        process_bar.set_process(10)
        if i[0] != '_Open_' and i[0] != '_Connect_':
            process_bar.set_process(20)
            my_serial.send_write_order([0x03, i[1]])
            process_bar.set_process(50)
            my_serial.send_write_order([0x0f, i[1]])
            my_serial.send_write_order([0x02, i[1], 0] + [0xff] * 15)
            process_bar.set_process(80)
            print(f'清除音频 {i[0]} 成功')
    my_serial.send_write_order([0x02, 63] + [0xff] * 16)
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (720, 110)}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (720, 110)}))
    process_bar.set_process(100)
    end_func = None

ba_filename = None
ba_data = {}
ba_state = 0    # 0：接收总音频数；1：接收数据包数；2：接收音频名称；3：接收音符轨道；4：接收时刻轨道
ba_temp1 = 0    # 总音频数
ba_temp2 = 0    # 音符数据包数
ba_temp3 = ''   # 音频名称
ba_temp4 = 0    # 时刻数据包数
ba_temp5 = 0    # 已接受音频数
backup_memory_button = MemoryButton(120, '备份音频', '备份存储的音频', center=(80, 200))
backup_memory_button.join(board)
def recv_backup_data(data):
    global ba_filename, ba_data, ba_state, ba_temp1, ba_temp2, ba_temp3, ba_temp4, ba_temp5

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
        process_bar.set_process(round(10 + 90 * ba_temp5 / ba_temp1, 1))
    elif ba_state == 1 and len(data) == 1:
        if data[0] == 0:    # 发送一个数据 0，表示结束备份
            ba_state = 0
            process_bar.set_process(100)
            with Path(ba_filename).open('wb') as f:
                print(ba_data)
                pickle.dump(ba_data, f)
            ba_filename = None
        else:
            ba_temp2 = ba_temp4 = data[0]
            ba_state = 2
            my_serial.send_read_order([0x04], recv_backup_data)
    elif ba_state == 0 and len(data) == 1:
        ba_temp1 = data[0]
        ba_state = 1
        my_serial.send_read_order([0x04], recv_backup_data)
        process_bar.set_process(5)
    else:
        ba_state = 0
        process_bar.set_process(0)

def backup_memory():
    global ba_filename, ba_data, ba_state
    ba_filename = asksaveasfilename(defaultextension='.mb', filetypes=[('Music Backup', '*.mb')], initialfile='music_backup.mb', title='备份音频', initialdir='./')
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (720, 110)}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (720, 110)}))
    if ba_filename:
        process_bar.set_process(10)
        ba_data = {}
        ba_state = 0
        my_serial.send_read_order([0x04], recv_backup_data)
    else:
        process_bar.set_process(0)
        ba_state = 0

im_filename = None
import_music_button = MemoryButton(120, '导入音频', '从文件导入音频', center=(240, 200))
import_music_button.join(board)
def import_music():
    global end_func
    end_func = import_music_
    process_bar.set_process(0)
    update_table()
import_music_button.bind(import_music)

def import_music_():
    global end_func, im_filename

    im_filename = askopenfilename(filetypes=[('Music Backup', '*.mb')], title='导入音频', initialdir='./')
    pygame.event.clear()
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (720, 110)}))
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (720, 110)}))
    if im_filename:
        with Path(im_filename).open('rb') as f:
            data = pickle.load(f)
        process_bar.set_process(10)
        for i in data:
            if i != '_Open_' and i != '_Connect_':
                process_bar.set_process(10)
                for page_num in range(60, 0, -1):
                    if flash_table_data[page_num * 16] == 0:
                        break
                else:
                    process_bar.set_process(10)
                    continue
                process_bar.set_process(20)
                my_serial.send_write_order([0x03, page_num])
                process_bar.set_process(30)
                for j in range(0, len(data[i][0]), 16):
                    my_serial.send_write_order([0x05, page_num, 32, j // 16, min(16, len(data[i][0]) - j)] + data[i][0][j: j + 16])
                    my_serial.send_write_order([0x05, page_num, 32, j // 16 + 16, min(16, len(data[i][0]) - j)] + data[i][1][j: j + 16])
                    process_bar.set_process(30 + 70 * j / len(data[i][0]))
                table_temp = [2] + [ord(j) for j in i] + [0] + [0xff] * (14 - len(i))
                my_serial.send_write_order([0x02, page_num] + table_temp)
                my_serial.send_write_order([0x02, 63] + [0xff] * 16)
                my_serial.send_write_order([0x10, page_num])
                flash_table_data[page_num * 16] = 2
                process_bar.set_process(100)
                print(f'导入音频 {i} 成功')
        process_bar.set_process(100)

    end_func = None


class DangerMemoryButton(MemoryButton):
    tstyle = get_text(24, FAKEWHITE)
    bcolors = dict(memory_button_color)
    bcolors['origin_bg'] = LIGHTRED
    bcolors['hover_bg'] = LIGHTRED + color_offset
    bcolors['press_bg'] = LIGHTRED - color_offset

    def __init__(self, width, text, tip_text, **anchor):
        super().__init__(width, text, tip_text, self.bcolors, **anchor)

ensure_flag = 0
erase_flash_button = DangerMemoryButton(220, '擦除全部程序数据', '仅在存储器被污染时使用此功能', center=(450, 200))
erase_flash_button.join(board)
def erase_flash():
    global ensure_flag
    if ensure_flag == 0:
        erase_flash_button.tip_text = '擦除后，需要重新烧录固件，请谨慎操作'
        set_tip_text1(erase_flash_button.tip_text)
        erase_flash_button.text.text = '危险操作！请确认'
        erase_flash_button.text.update_img()
        ensure_flag = 1
        cancel_trigger.launch(180)
        process_bar.set_process(50)
        erase_flash_button.bind(erase_flash)
    elif ensure_flag == 1:
        cancel_trigger.stop()
        cancel_erase()
        my_serial.send_write_order([0x04])
        process_bar.set_process(100)
def cancel_erase():
    global ensure_flag
    erase_flash_button.tip_text = '仅在存储器被污染时使用此功能'
    if erase_flash_button.mousewidget.mouseon:
        set_tip_text1(erase_flash_button.tip_text)
    erase_flash_button.text.text = '擦除全部程序数据'
    erase_flash_button.text.update_img()
    ensure_flag = 0
    process_bar.set_process(0)
    erase_flash_button.bind(process_bar.set_process, 0, erase_flash)
cancel_trigger = fantas.Trigger(cancel_erase)


class ProcessBar(fantas.Label):
    height = 20
    width = 400
    bar_bg = LIGHTGRAY - color_offset
    bar_fg = LIGHTBLUE
    tstyle = get_text(16, DEEPBLUE)

    def __init__(self, **anchor):
        super().__init__((self.width, self.height), bg=self.bar_bg, radius={'border_radius': 4}, **anchor)
        self.bar = fantas.Label((0, self.height), bg=self.bar_fg, radius={'border_radius': 4}, topleft=(0, 0))
        self.bar.join(self)
        self.bar.anchor = 'topleft'
        self.bar_size_kf = fantas.LabelKeyFrame(self.bar, 'size', 0, 12, u.slower_curve)
        self.percent_text = fantas.Text('0% ', u.fonts['shuhei'], self.tstyle, center=(0, self.height // 2))
        self.percent_text_pos_kf = fantas.RectKeyFrame(self.percent_text, 'right', 0, 12, u.faster_curve)

    def set_process(self, percent, func=None, *args, **kwargs):
        percent = min(max(round(percent, 1), 0), 100)
        self.bar_size_kf.value = (self.width * percent / 100, self.height)
        self.bar_size_kf.launch('continue')
        self.percent_text.text = f'{percent}% '
        self.percent_text.update_img()
        if self.bar_size_kf.value[0] > self.percent_text.rect.width:
            if self.percent_text.is_root():
                self.percent_text.join(self)
        elif not self.percent_text.is_root():
            self.percent_text.leave()
        self.percent_text_pos_kf.value = self.bar_size_kf.value[0]
        self.percent_text_pos_kf.launch('continue')
        self.percent_text_pos_kf.bind_endupwith(func, *args, **kwargs)

process_bar = ProcessBar(center=(u.WIDTH // 2 - 113, 268))
process_bar.join(board)

export_table_button.bind(process_bar.set_process, 0, export_table)
erase_flash_button.bind(process_bar.set_process, 0, erase_flash)
import_table_button.bind(process_bar.set_process, 0, import_table)
backup_memory_button.bind(process_bar.set_process, 0, backup_memory)
