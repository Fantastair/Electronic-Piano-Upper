import pygame
import pygame.freetype
import webbrowser

import fantas
from fantas import uimanager
u = uimanager

# ==============================


class ColorButtonMouseWidget(fantas.AnyButton):
	# 变色按钮的搭配组件

	__slots__ = []

	def __init__(self, ui):
		super().__init__(ui, 2)

	def mousein(self):
		# 鼠标移入变色
		u.set_cursor('hand')
		if self.mousedown == 1:
			self.ui.set_state('press')
		else:
			self.ui.set_state('hover')

	def mouseout(self):
		# 鼠标移出变色
		u.set_cursor_back()
		self.ui.set_state('origin')

	def mousepress(self, pos, button):
		# 左键按下变色
		if self.mousedown == 1:
			self.ui.set_state('press')

	def mouserelease(self, pos, button):
		# 鼠标松开变色
		if self.mouseon:
			self.ui.set_state('hover')

class ColorButtonKeyWidget(fantas.KeyboardBase):
	__slots__ = ['pressed']

	def keyboardpress(self, key, shortcut):
		if shortcut == self.ui.shortcut:
			self.pressed = True
		elif shortcut == self.ui.cancel_key and self.pressed:
			self.pressed = False

	def keyboardrelease(self, key, shortcut):
		if self.pressed and shortcut == self.ui.shortcut:
			self.ui.mousewidget.func(*self.ui.mousewidget.args, **self.ui.mousewidget.kwargs)
			self.pressed = False


class ColorButton(fantas.Label):
	# 变色按钮，悬浮和按下有颜色反馈

	__slots__ = ['colors', 'mousewidget', 'is_banned', 'shortcut', 'cancel_key', 'keywidget', 'keywidget_class']

	def __init__(self, size, colors, bd=0, mousewidget=ColorButtonMouseWidget, keywidget=ColorButtonKeyWidget, cancel_key='escape', **kwargs):
		super().__init__(size, bd, colors['origin_bg'], None if 'origin_sc' not in colors else colors['origin_sc'], **kwargs)
		self.colors = colors
		self.mousewidget = mousewidget(self)
		self.keywidget_class = keywidget
		self.mousewidget.apply_event()
		self.is_banned = False
		self.shortcut = None
		self.cancel_key = cancel_key

	def ban(self):
		# 禁用按钮
		self.is_banned = True
		self.mousewidget.cancel_event()
		if self.shortcut is not None:
			self.keywidget.cancel_event()
		self.set_state('ban')

	def recover(self):
		# 恢复按钮
		self.is_banned = False
		self.mousewidget.apply_event()
		if self.shortcut is not None:
			self.keywidget.apply_event()
		self.set_state('origin')

	def bind(self, func, *args, **kwargs):
		self.mousewidget.bind(func, *args, **kwargs)

	def bind_shortcut(self, shortcut):
		if self.shortcut is None:
			self.keywidget = self.keywidget_class(self)
			self.keywidget.pressed = False
			if not self.is_banned:
				self.keywidget.apply_event()
		self.shortcut = shortcut

	def set_state(self, key):
		# 根据关键字设置样式
		self.set_bg(self.colors[f'{key}_bg'])
		if self.bd > 0:
			self.set_sc(self.colors[f'{key}_sc'])


class SmoothColorButton(ColorButton):
	__slots__ = ['feedback_bg', 'feedback_bd', 'feedback_sc']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.feedback_bg = fantas.LabelKeyFrame(self, 'bg', self.colors['origin_bg'], 10, u.harmonic_curve)
		self.feedback_bd = fantas.LabelKeyFrame(self, 'bd', self.bd, 10, u.harmonic_curve)
		self.feedback_sc = fantas.LabelKeyFrame(self, 'sc', self.colors['origin_bg'], 10, u.harmonic_curve)

	def set_state(self, key):
		if key == 'hover':
			self.feedback_bg.totalframe = 10
		elif key == 'press':
			self.feedback_bg.totalframe = 5
		elif key == 'origin':
			self.feedback_bg.totalframe = 16
		self.feedback_bg.value = self.colors[f'{key}_bg']
		if self.feedback_bg.value is not None:
			self.feedback_bg.launch('continue')
		if self.colors.get(f'{key}_bd', 0) > 0:
			self.feedback_bd.value = self.colors[f'{key}_bd']
			self.feedback_sc.value = self.colors[f'{key}_sc']
			if key == 'hover':
				self.feedback_bd.totalframe = 10
				self.feedback_sc.totalframe = 10
			elif key == 'press':
				self.feedback_bd.totalframe = 5
				self.feedback_sc.totalframe = 5
			elif key == 'origin':
				self.feedback_bd.totalframe = 16
				self.feedback_sc.totalframe = 16
			self.feedback_bd.launch('continue')
			self.feedback_sc.launch('continue')

# ==============================
'''

class MenuBarMouseWidget(fantas.MouseBase):
	__slots__ = []

	def __init__(self, ui):
		super().__init__(ui, 2)

	def mousepress(self, pos):
		if self.ui.son_menu_opened is not None and (self.mouseon and pos[0] > self.ui.pos or not self.ui.son_menu_opened.menu.rect.collidepoint(pos)):
			if self.ui.keywidget.choose_menu:
				self.ui.keywidget.keyboardpress('left alt', 'Alt')
			else:
				self.ui.son_menu_opened.close_menu()


class MenuBarKeyWidget(fantas.KeyboardBase):
	__slots__ = ['choose_menu', 'global_key']

	def __init__(self, ui):
		super().__init__(ui)
		self.choose_menu = False
		self.global_key = {}

	def keyboardpress(self, key, shortcut):
		if shortcut in self.global_key:
			self = self.global_key[shortcut].mousewidget
			if not self.ui.is_banned:
				self.func(*self.args, **self.kwargs)
				if self.ui.menu.menubar.keywidget.choose_menu:
					self.ui.menu.menubar.keywidget.keyboardpress('left alt', 'Alt')
				else:
					self.ui.menu.close_menu()
		elif self.ui.son_menu_opened is not None and self.ui.son_menu_opened.local_key is not None and shortcut in self.ui.son_menu_opened.local_key:
			self = self.ui.son_menu_opened.local_key[shortcut].mousewidget
			if not self.ui.is_banned:
				self.func(*self.args, **self.kwargs)
				if self.ui.menu.menubar.keywidget.choose_menu:
					self.ui.menu.menubar.keywidget.keyboardpress('left alt', 'Alt')
				else:
					self.ui.menu.close_menu()
		elif shortcut == 'Alt':
			self.choose_menu = not self.choose_menu
			if self.choose_menu:
				self.ui.textstyle['style'] += pygame.freetype.STYLE_UNDERLINE
				for m in self.ui.menus:
					self.ui.menus[m].text.update_img()
				self.ui.textstyle['style'] -= pygame.freetype.STYLE_UNDERLINE
			else:
				for m in self.ui.menus:
					self.ui.menus[m].text.update_img()
				if self.ui.son_menu_opened is not None:
					self.ui.son_menu_opened.close_menu()
		elif self.choose_menu:
			if shortcut in self.ui.alt_map:
				self.ui.menus[self.ui.alt_map[shortcut]].mousewidget.mousein()
				self.ui.menus[self.ui.alt_map[shortcut]].open_menu()
			elif shortcut[4:] in self.ui.alt_map:
				self.ui.menus[self.ui.alt_map[shortcut[4:]]].mousewidget.mousein()
				self.ui.menus[self.ui.alt_map[shortcut[4:]]].open_menu()
			else:
				self.keyboardpress('left alt', 'Alt')


class MenuBar(fantas.Label):
	# 菜单栏
	__slots__ = ['son_menu_opened', 'menu_colors', 'item_style', 'textstyle', 'menu_width', 'font', 'menus', 'pos', 'mousewidget', 'keywidget', 'alt_map']

	def __init__(self, size, menu_width, font, style, mousewidget=MenuBarMouseWidget, keywidget=MenuBarKeyWidget, **kwargs):
		self.son_menu_opened = None
		self.menu_colors, self.item_style, self.textstyle = style
		super().__init__(size, bg=self.menu_colors['origin_bg'], **kwargs)
		self.menu_width = menu_width
		self.font = font
		self.menus = {}
		self.alt_map = {}
		self.pos = 0
		self.mousewidget = mousewidget(self)
		self.keywidget = keywidget(self)
		self.mousewidget.apply_event()
		self.keywidget.apply_event()

	def add_menu(self, name, menu_width=None, alt=None):
		# 添加菜单
		if menu_width is None:
			menu_width = self.menu_width
		if alt is not None:
			self.alt_map[alt] = name
		c = MenuButton(self, f'{name}({alt})', (menu_width,self.origin_size[1]), self.menu_colors, left=self.pos)
		c.join(self)
		self.pos += menu_width
		self.menus[name] = c

	def del_menu(self, name):
		# 删除菜单
		m = self.menus[name]
		m.leave()
		self.pos -= m.rect.width
		self.menus.remove(m)
		self.alt_map.remove(name)

	def open_menu(self, name):
		# 开启菜单
		if self.son_menu_opened is not None:
			if name == self.son_menu_opened.name:
				return
			else:
				self.son_menu_opened.close_menu()
		self.menus[name].open_menu()

	def close_menu(self):
		# 关闭菜单
		if self.son_menu_opened is not None:
			self.son_menu_opened.close_menu()


class MenuButtonWidget(ColorButtonMouseWidget):
	__slots__ = []

	def mouseout(self):
		if not self.ui.opened:
			super().mouseout()

	def mousein(self):
		if not self.ui.opened:
			super().mousein()
			if self.ui.menubar.son_menu_opened is not None and self is not self.ui.menubar.son_menu_opened:
				self.ui.menubar.son_menu_opened.close_menu()
				self.ui.open_menu()

	def handle(self, event):
		if event.type == pygame.WINDOWLEAVE:
			if self.mouseon:
				self.mouseon = False
				self.mouseout()
		else:
			super().handle(event)


class MenuButton(ColorButton):
	__slots__ = ['opened', 'menubar', 'name', 'items', 'item_style', 'text', 'menu', 'pos', 'local_key']

	def __init__(self, menubar, name, size, colors, item_style=None, **kwargs):
		super().__init__(size, colors, mousewidget=MenuButtonWidget, **kwargs)
		self.opened = False
		self.menubar = menubar
		self.items = {}
		self.local_key = None
		if item_style is None:
			self.item_style = self.menubar.item_style
		else:
			self.item_style = item_style
		self.text = fantas.Text(name, menubar.font, menubar.textstyle, center=(size[0]//2,size[1]//2))
		self.text.join(self)
		self.menu = fantas.Label((0,0), bg=self.item_style['origin_bg'], bd=self.item_style['bd'], sc=self.item_style['sc'])
		self.bind(self.open_menu)
		self.pos = self.item_style['sidepad']

	def open_menu(self):
		self.opened = True
		self.menu.rect.topleft = (self.menubar.rect.left+max(self.rect.left,0), self.menubar.rect.bottom)
		if self.menu.father is None:
			if self.is_root():
				self.menu.join(self)
				self.apply_event(self.menu)
			else:
				self.menu.join(self.father)
				self.father.apply_event(self.menu)
			pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, {'pos': pygame.mouse.get_pos()}))
		if self.menubar.son_menu_opened is not None and self.menubar.son_menu_opened is not self:
			self.menubar.son_menu_opened.close_menu()
		self.menubar.son_menu_opened = self
		self.bind(self.close_menu)

	def close_menu(self):
		if self.menubar.son_menu_opened is not None:
			self.opened = False
			self.set_bg(self.menubar.menu_colors['origin_bg'])
			self.menu.leave()
			self.menubar.son_menu_opened = None
			self.bind(self.open_menu)

	def add_item(self, item, func=None, *args, **kwargs):
		# 添加项
		c = fantas.MenuItem(self, item, (self.item_style['width'],self.menubar.origin_size[1]), self.item_style, mousewidget=MenuItemWidget, topleft=(self.item_style['sidepad'],self.pos))
		self.pos += c.rect.h
		c.join(self.menu)
		self.menu.set_size((self.item_style['boxwidth'], self.pos+self.item_style['sidepad']))
		self.items[item] = c
		if func is not None:
			c.bind(func, *args, **kwargs)
		else:
			self.ban_item(item)

	def add_splitline(self):
		l = fantas.Label((self.item_style['width'],self.item_style['lineheight']), bd=self.item_style['linebd'], bg=self.item_style['sc'], sc=self.item_style['origin_bg'], topleft=(self.item_style['sidepad'],self.pos))
		self.pos += l.rect.h
		l.join(self.menu)
		self.menu.set_size((self.item_style['boxwidth'], self.pos+self.item_style['sidepad']))

	def ban_item(self, item):
		self.items[item].ban()
		self.menubar.textstyle['fgcolor'] = self.item_style['ban']
		self.items[item].text.update_img()
		if self.items[item].shortcut_text is not None:
			self.items[item].shortcut_text.update_img()
		self.menubar.textstyle['fgcolor'] = self.item_style['normal']

	def recover_item(self, item):
		self.items[item].recover()
		self.items[item].text.update_img()
		if self.items[item].shortcut_text is not None:
			self.items[item].shortcut_text.update_img()

	def bind_shortcut(self, item, shortcut, global_=True):
		if global_:
			self.menubar.keywidget.global_key[shortcut] = self.items[item]
			if self.items[item].is_banned:
				self.menubar.textstyle['fgcolor'] = self.item_style['ban']
			self.items[item].shortcut_text = fantas.Text(shortcut, self.menubar.font, self.menubar.textstyle, midright=(self.items[item].rect.w-self.item_style['rightpad'],self.items[item].rect.h//2))
			self.items[item].shortcut_text.join(self.items[item])
			if self.items[item].is_banned:
				self.menubar.textstyle['fgcolor'] = self.item_style['normal']
		else:
			if self.local_key is None:
				self.local_key = {shortcut: self.items[item]}
			else:
				self.local_key[shortcut] = self.items[item]
			self.items[item].text.text += f'({shortcut})'
			if self.items[item].is_banned:
				self.menubar.textstyle['fgcolor'] = self.item_style['ban']
				self.items[item].text.update_img()
				self.menubar.textstyle['fgcolor'] = self.item_style['normal']
			else:
				self.items[item].text.update_img()

class MenuItem(ColorButton):
	__slots__ = ['menu', 'item', 'text', 'shortcut_text']

	def __init__(self, menu, item, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.menu = menu
		self.item = item
		self.text = fantas.Text(item, self.menu.menubar.font, self.menu.menubar.textstyle, midleft=(self.menu.item_style['leftpad'],self.rect.h//2))
		self.text.join(self)
		self.text.anchor = 'midleft'
		self.shortcut_text = None


class MenuItemWidget(ColorButtonMouseWidget):
	__slots__ = []

	def mouseclick(self):
		if self.mousedown == 1:
			self.func(*self.args, **self.kwargs)
			if self.ui.menu.menubar.keywidget.choose_menu:
				self.ui.menu.menubar.keywidget.keyboardpress('left alt', 'Alt')
			else:
				self.ui.menu.close_menu()

'''
# ==============================


class WebURL(fantas.Text):
	# 网站跳转链接
	__slots__ = ['url', 'mousewidget']

	def __init__(self, text, url, *args, **kwargs):
		super().__init__(text, *args, **kwargs)
		if 'style' not in self.style:
			self.style['style'] = pygame.freetype.STYLE_NORMAL
		self.url = url
		self.mousewidget = WebURL_Widget(self, 2)
		self.mousewidget.bind(webbrowser.open, self.url)
		self.mousewidget.apply_event()


class WebURL_Widget(fantas.AnyButton):
	def mousein(self):
		u.set_cursor('hand')
		self.ui.style['style'] += pygame.freetype.STYLE_UNDERLINE
		self.ui.update_img()
		self.ui.style['style'] -= pygame.freetype.STYLE_UNDERLINE

	def mouseout(self):
		u.set_cursor_back()
		self.ui.update_img()


# ==============================
# '''

class InputLine(fantas.Label):
	# 单行输入框

	__slots__ = ['font', 'style', 'textstyle', 'maxinput', 'startpos', 'endpos', 'cursor', 'cursorpos', 'editing', 'text', 'tiptext', 'inputwidget', 'mousewidget', 'keywidget', 'move_cursor', 'shake_cursor', 'inputed_text', 'inputed_pos']

	def __init__(self, size, font, style, textstyle, tiptext=None, maxinput=None, **kwargs):
		super().__init__(size, **kwargs)
		self.font = font
		self.style = style
		self.textstyle = textstyle
		self.maxinput = maxinput
		self.startpos = style['text_pad']
		self.endpos = self.origin_size[0] - self.startpos
		self.cursor = fantas.Label(style['cursor_size'], bg=style['cursor_bg'], midleft=(self.startpos,self.origin_size[1]/2))
		self.cursorpos = 0
		self.editing = False
		self.text = fantas.Text('', font, textstyle, midleft=(self.startpos,self.origin_size[1]/2))
		self.text.anchor = 'midleft'
		self.text.join(self)
		if tiptext is not None:
			self.tiptext = fantas.Text(tiptext, font, dict(textstyle), midleft=(self.startpos,self.origin_size[1]/2))
			self.tiptext.join(self)
		else:
			self.tiptext = None
		self.inputwidget = InputLineWidget(self)
		self.mousewidget = InputLineMouseWidget(self, 2)
		self.keywidget = InputLineKeyWidget(self)
		self.mousewidget.apply_event()
		self.move_cursor = fantas.RectKeyFrame(self.cursor, 'left', self.startpos, 6, u.harmonic_curve)
		self.shake_cursor = fantas.RectKeyFrame(self.cursor, 'left', 6, 12, u.sin_curve, absolute=False)

	def adapt(self):
		# 将光标移动到正确的位置
		if self.cursorpos == len(self.text.text):
			self.move_cursor.value = self.text.rect.right
		else:
			self.move_cursor.value = self.font.get_rect(self.text.text[:self.cursorpos], size=self.textstyle['size']).width + self.text.rect.left
		if self.move_cursor.value < self.startpos:
			offset = self.startpos - self.move_cursor.value
			self.move_cursor.value += offset
			self.text.rect.left += offset
		elif self.move_cursor.value+self.cursor.rect.width > self.endpos:
			offset = self.move_cursor.value+self.cursor.rect.width - self.endpos
			self.move_cursor.value -= offset
			self.text.rect.left -= offset
		self.move_cursor.launch(flag='continue')
		if self.tiptext is not None and self.text.text != '' and self.tiptext.father is self:
			self.tiptext.leave()

	def get_input(self):
		# 获取当前输入
		return self.text.text

	def clear(self):
		# 清空当前输入
		self.text.text = ''
		self.text.update_img()
		self.cursorpos = 0
		self.cursor.rect.left = self.startpos
		self.editing = False
		if self.tiptext is not None and self.tiptext.father is None:
			self.tiptext.join(self)

class InputLineWidget(fantas.TextInputBase):
	__slots__ = []

	def textinput(self, text):
		if self.ui.editing:
			if self.ui.maxinput is not None:
				over = self.ui.maxinput - len(self.ui.inputed_text + text)
				if over < 0:
					text = text[:over]
			self.ui.cursorpos = self.ui.inputed_pos
			self.ui.text.text = self.ui.inputed_text[:self.ui.inputed_pos] + text + self.ui.inputed_text[self.ui.inputed_pos:]
			self.ui.editing = False
		else:
			if self.ui.maxinput is not None:
				over = self.ui.maxinput - len(self.ui.text.text + text)
				if over < 0:
					text = text[:over]
			self.ui.text.text = self.ui.text.text[:self.ui.cursorpos] + text + self.ui.text.text[self.ui.cursorpos:]
		self.ui.text.update_img()
		self.ui.cursorpos += len(text)
		self.ui.adapt()
		if self.ui.maxinput is not None:
			if over < 0:
				self.ui.move_cursor.stop()
				self.ui.shake_cursor.launch(start=self.ui.move_cursor.value, flag='restart')

	def textedit(self, text, start):
		if not self.ui.editing:
			self.ui.editing = True
			self.ui.inputed_text = self.ui.text.text
			self.ui.inputed_pos = self.ui.cursorpos
		self.ui.text.text = self.ui.inputed_text[:self.ui.inputed_pos] + text + self.ui.inputed_text[self.ui.inputed_pos:]
		self.ui.text.update_img()
		self.ui.cursorpos = self.ui.inputed_pos + start
		self.ui.adapt()

	def start_input(self):
		super().start_input()
		self.ui.cursor.join(self.ui)
		self.ui.keywidget.apply_event()
		pygame.key.set_repeat(300, 50)

	def stop_input(self):
		super().stop_input()
		self.ui.cursor.leave()
		self.ui.keywidget.cancel_event()
		pygame.key.set_repeat()

class InputLineMouseWidget(fantas.MouseBase):
	__slots__ = []

	def mousepress(self, pos, button):
		if button == 1:
			if self.ui.inputwidget.inputing:
				if not self.ui.rect.collidepoint(pos):
					self.ui.inputwidget.stop_input()
			elif self.ui.rect.collidepoint(pos):
				self.ui.inputwidget.start_input()

	def mousein(self):
		u.set_cursor('I')

	def mouseout(self):
		u.set_cursor_back()

class InputLineKeyWidget(fantas.KeyboardBase):
	__slots__ = []

	def keyboardpress(self, key, shortcut):
		if key == 'backspace':
			if self.ui.text.text and self.ui.cursorpos != 0:
				if shortcut == 'Backspace':
					self.ui.text.text = self.ui.text.text[:self.ui.cursorpos-1] + self.ui.text.text[self.ui.cursorpos:]
					self.ui.cursorpos -= 1
				elif shortcut == 'Ctrl+Backspace':
					self.ui.text.text = self.ui.text.text[self.ui.cursorpos:]
					self.ui.cursorpos = 0
				if self.ui.tiptext is not None and self.ui.text.text == '':
					self.ui.tiptext.join(self.ui)
				self.ui.text.update_img()
				self.ui.adapt()
		elif shortcut == 'Left':
			self.ui.cursorpos -= 1
			self.ui.cursorpos = max(self.ui.cursorpos, 0)
			self.ui.adapt()
			self.ui.mark_update()
		elif shortcut == 'Right':
			self.ui.cursorpos += 1
			self.ui.cursorpos = min(self.ui.cursorpos, len(self.ui.text.text))
			self.ui.adapt()
			self.ui.mark_update()
		elif shortcut == 'Up' or shortcut == 'Ctrl+Left':
			self.ui.cursorpos = 0
			self.ui.adapt()
			self.ui.mark_update()
		elif shortcut == 'Down' or shortcut == 'Ctrl+Right':
			self.ui.cursorpos = len(self.ui.text.text)
			self.ui.adapt()
			self.ui.mark_update()
'''


class ProcessBarMouseWidget(fantas.MouseBase):
	__slots__ = ()

	def mousepress(self, pos, button):
		if button == 1:
			if self.ui.block.rect.collidepoint(pos):
				self.mousedown = 1
			elif self.mouseon:
				pos = pos[0] if self.ui.xy[-1] == 'x' else pos[1]
				self.ui.set_pos(pos)

	def mousemove(self, pos):
		if self.mousedown == 1:
			pos, extent = (pos[0], (self.ui.rect.left,self.ui.rect.right)) if self.ui.xy[-1] == 'x' else (pos[1], (self.ui.rect.top,self.ui.rect.bottom))
			if pos < extent[0]:
				pos = extent[0]
			if pos > extent[1]:
				pos = extent[1]
			self.ui.set_pos(pos, smooth=False)


class ProcessBar(fantas.Label):
	# 滚动条
	__slots__ = ('extent', 'data', 'xy', 'block', 'style', 'cover_bar', 'move_block', 'mousewidget', 'scale_cover')
	xy_map = {'x': 'left', 'y': 'top', '-x': 'right', '-y': 'bottom'}

	def __init__(self, extent, xy: str, block: fantas.Label, style, size, **kwargs):
		# extent 表示数据域：(起点, 长度)
		# xy 用于指定方向，有4种选择，x(左>右) y(上>下) -x(右>左) -y(下>上)
		super().__init__(size, bg=style['origin_bg'], **kwargs)
		self.extent = extent
		self.data = None
		self.xy = xy
		self.block = block
		self.block.rect.center = self.rect.center
		self.style = style
		r = dict(self.radius)
		for s in r:
			r[s] = r[s] - self.bd
		self.cover_bar = fantas.Label((self.rect.w-self.bd*2,self.rect.h-self.bd*2), bg=style['set_bg'], radius=r)
		self.cover_bar.anchor = 'topleft' if xy[-1] != '-' else 'bottomright'
		setattr(self.cover_bar.rect, 'topleft' if xy[-1] != '-' else 'bottomright', (self.bd,self.bd) if xy[-1]!='-' else (self.rect.w-self.bd,self.rect.h-self.bd))
		self.cover_bar.join(self)
		self.scale_cover = fantas.LabelKeyFrame(self.cover_bar, 'size', None, 10, u.harmonic_curve)
		self.move_block = fantas.RectKeyFrame(self.block, f'center{xy[-1]}', None, 10, u.harmonic_curve)
		self.mousewidget = ProcessBarMouseWidget(self, 3)
		self.mousewidget.apply_event()

	def join(self, father):
		super().join(father)
		self.block.join(father)

	def leave(self):
		super().leave()
		self.block.leave()

	def set_pos(self, pos, smooth=True, set_data=True):
		# 设置位置
		# 未进行边界检查，手动调用时注意
		if smooth:
			self.scale_cover.value = (abs(pos-getattr(self.rect,self.xy_map[self.xy])), getattr(self.cover_bar.rect, 'h' if self.xy[-1]=='x' else 'w'))
			if self.xy[-1] != 'x':
				self.scale_cover.value = self.scale_cover.value[1], self.scale_cover.value[0]
			self.move_block.value = pos
			self.scale_cover.launch('continue')
			self.move_block.launch('continue')
		else:
			if self.scale_cover.is_launched():
				self.scale_cover.stop()
				self.move_block.stop()
			size = (abs(pos-getattr(self.rect,self.xy_map[self.xy])), getattr(self.cover_bar.rect, 'h' if self.xy[-1]=='x' else 'w'))
			if self.xy[-1] != 'x':
				size = size[1], size[0]
			self.cover_bar.set_size(size)
			setattr(self.block.rect, f'center{self.xy[-1]}', pos)
			self.cover_bar.mark_update()
			self.block.mark_update()
		if set_data:
			pos_extent, pos_len = ((self.rect.left,self.rect.right), self.rect.width) if self.xy[-1] == 'x' else ((self.rect.top,self.rect.bottom), self.rect.height)
			if self.xy[0] == '-':
				pos_extent = pos_extent[1]
				pos_len = - pos_len
			else:
				pos_extent = pos_extent[0]
			r = (pos - pos_extent) / pos_len
			data = self.extent[0] + self.extent[1] * r
			self.set_data(data)

	def set_data(self, data, smooth=True, set_pos=False):
		# 设置参数
		# 子类决定如何影响外部
		# 未进行边界检查，手动调用时注意
		data = round(data)
		self.data = data
		if set_pos:
			r = (data-self.extent[0]) / self.extent[1]
			pos_extent, pos_len = ((self.rect.left,self.rect.right), self.rect.width) if self.xy[-1] == 'x' else ((self.rect.top,self.rect.bottom), self.rect.height)
			if self.xy[0] == '-':
				pos_extent = pos_extent[1]
				pos_len = - pos_len
			else:
				pos_extent = pos_extent[0]
			pos = pos_extent + pos_len * r
			self.set_pos(pos, smooth, set_data=False)

	def get_data(self):
		# 获取当前设置数据
		return self.data


class TickBox(fantas.Label):
	# 勾选框
	__slots__ = ('size_', 'style', 'choose_flag', 'tick_style', 'tick_text', 'scale_bd', 'mousewidget', 'assistant', 'choose')

	def __init__(self, size, tick_chr: str, tick_font, tick_size, style, choose, offset=None, **kwargs):
		super().__init__((size,size), bg=style['origin_bg'], bd=style['origin_bd'], sc=style['origin_sc'], **kwargs)
		self.size_ = size
		self.style = style
		self.choose_flag = False
		self.tick_style = {'size': tick_size, 'fgcolor': style['origin_sc']}
		self.tick_text = fantas.Text(tick_chr, tick_font, self.tick_style,
			center=(self.rect.width/2,self.rect.height/2) if offset is None else (self.rect.width/2+offset[0],self.rect.height/2+offset[1]))
		self.scale_bd = fantas.LabelKeyFrame(self, 'bd', None, 7, u.curve)
		self.mousewidget = fantas.AnyButton(self)
		self.mousewidget.bind(self.click)
		self.mousewidget.apply_event()
		self.assistant = None
		self.choose = choose

	def click(self):
		self.choose_flag = not self.choose_flag
		self.choose(self.choose_flag)
		self.scale_bd.bind_endupwith(self.middle)
		self.scale_bd.value = self.size_ / 2
		self.scale_bd.launch('continue')
		if self.choose_flag:
			self.set_bg(self.style['chose_bg'])
			self.set_sc(self.style['chose_sc'])
			self.tick_style['fgcolor'] = self.style['chose_sc']
			self.tick_text.update_img()
		else:
			self.set_bg(self.style['origin_bg'])
			self.set_sc(self.style['origin_sc'])
			self.tick_style['fgcolor'] = self.style['origin_sc']
			self.tick_text.update_img()

	def middle(self):
		if self.choose_flag:
			self.tick_text.join(self)
		else:
			self.tick_text.leave()
		self.scale_bd.bind_endupwith(None)
		self.scale_bd.value = self.style['origin_bd']
		self.scale_bd.launch('continue')

	def set_assist_click(self, ui: fantas.Ui):
		# 设置对 ui 的点击动作映射到自己身上，方便点击
		if self.assistant is None:
			self.assistant = []
		a = fantas.AnyButton(ui)
		a.bind(self.click)
		self.assistant.append(a)
		a.apply_event()

	def cancel_assist_click(self, ui: fantas.Ui):
		# 取消 ui 的辅助点按
		for a in self.assistant:
			if a.ui is ui:
				self.assistant.remove(a)
				a.cancel_event()
				return

# '''
