import pygame
import pygame.freetype
import fantas
from fantas import uimanager
u = uimanager

'''
def split_img(img, size):
	# 将原始图像分隔为size大小的连续帧
	result = []
	r = pygame.Rect((0,0),size)
	w, h = img.get_size()
	w, h = w//size[0], h//size[1]
	for y in range(h):
		r.top = y*size[1]
		for x in range(w):
			r.left = x*size[0]
			result.append(img.subsurface(r))
	return result


class FrameAnimation(fantas.Ui):
	# 帧动画，使用关键帧控制播放

	__slots__ = ['currentframe', 'length', 'img_list', 'img']

	def __init__(self, img_list, **kwargs):
		super().__init__(img_list[0], **kwargs)
		self.currentframe = 0
		self.length = len(img_list)
		self.img_list = img_list

	def set_frame(self, frame):
		# 设置当前帧
		self.currentframe = frame
		self.img = self.img_list[frame]
		self.mark_update()

	def next_frame(self, n=1):
		# 向后切换帧，默认为1帧
		self.currentframe += n
		self.currentframe %= self.length
		self.set_frame(self.currentframe)
'''

class Label(fantas.Ui):
	# 矩形标签，提供了纯色背景和矩形边框(可设置圆角)
	# 可以自定义内部元素并控制其相对位置

	__slots__ = ('bd', 'bg', 'sc', 'layout_data', 'radius_')

	def __init__(self, size, bd=0, bg=None, sc=None, radius=None, **anchor):
		fantas.NodeBase.__init__(self)
		self.bg, self.sc, self.bd, self.layout_data = bg, sc, bd, None
		if radius is None:
			self.radius_ = {}
		else:
			self.radius_ = radius
		self.size = self.origin_size = size
		self.anchor = 'center'
		self.temp_img = self.img = pygame.Surface(self.origin_size, flags=pygame.SRCALPHA)
		if self.bg is not None:
			pygame.draw.rect(self.img, self.bg, self.img.get_rect(), **self.radius_)
		if self.bd > 0 and self.sc is not None:
			pygame.draw.rect(self.img, self.sc, (0,0,*self.origin_size), width=round(self.bd), **self.radius_)
		self.angle = 0
		self.alpha = self.origin_alpha = 255
		self.update_flag = True
		self.widgetgroup = None
		self.rect = self.img.get_rect(**anchor)

	def render(self, target=None):
		if self.update_flag:
			self.update_img()
		super().render(target)
	
	def _get_radius(self):
		return self.radius_.get('border_radius')
	
	def _set_radius(self, value):
		self.radius_['border_radius'] = value
	
	radius = property(_get_radius, _set_radius)

	def update_img(self):
		self.temp_img = self.img = pygame.Surface(self.origin_size, flags=pygame.SRCALPHA)
		if self.bg is not None:
			pygame.draw.rect(self.img, self.bg, self.img.get_rect(), **self.radius_)
		if self.bd > 0 and self.sc is not None:
			pygame.draw.rect(self.img, self.sc, (0,0,*self.origin_size), width=round(self.bd), **self.radius_)
		self.update_rect()
		self.layout()

	def set_size(self, size):
		# 设置大小
		self.origin_size = self.size = size
		pos = getattr(self.rect, self.anchor)
		self.rect.size = size
		setattr(self.rect, self.anchor, pos)
		self.mark_update()

	def set_radius(self, r):
		self.radius_['border_radius'] = round(r)
		self.mark_update()

	def set_bg(self, bg):
		# 设置背景色
		self.bg = bg
		self.mark_update()

	def set_sc(self, sc):
		# 设置边框色
		self.sc = sc
		self.mark_update()

	def set_bd(self, bd):
		# 设置边框粗细
		self.bd = bd
		self.mark_update()

	def set_layout(self, ui, data):
		# 设置布局参数
		if self.layout_data is None:
			self.layout_data = {}
		if ui in self.layout_data:
			self.layout_data[ui].append(data)
		else:
			self.layout_data[ui] = [data]

	def layout(self):
		# 重新布局
		# 参数示例：('rect', 'center', (100,100))
		#           模式     属性        数据
		if self.layout_data is not None:
			for ui in self.layout_data:
				for data in self.layout_data[ui]:
					if data[0] == 'pos':  # 固定坐标
						setattr(ui.rect, data[1], data[2])
					elif data[0] == 'fx':  # 相对右端坐标
						setattr(ui.rect, data[1], self.rect.width+data[2])
					elif data[0] == 'fy':  # 相对底端坐标
						setattr(ui.rect, data[1], self.rect.height+data[2])
					elif data[0] == 'x':  # 固定x轴比例
						setattr(ui.rect, data[1], self.rect.width*data[2])
					elif data[0] == 'y':  # 固定y轴比例
						setattr(ui.rect, data[1], self.rect.height*data[2])
					elif data[0] == 'xy':  # 二维比例
						setattr(ui.rect, data[1], fantas.tuple_operate(self.size, data[2], fantas.mul))


class Text(fantas.Ui):
	# 单行文本，统一样式

	__slots__ = ['text', 'font', 'style']

	def __init__(self, text, font, style, **kwargs):
		# style = {'fgcolor', 'bgcolor', 'style', 'size', 'rotation'}
		# 可省略但不能多
		self.text = text
		self.font = font
		self.style = style
		super().__init__(self.draw_text(), **kwargs)

	def update_img(self):
		# 更新图像
		self.img = self.temp_img = self.draw_text()
		self.update_rect()
		self.mark_update()

	def draw_text(self):
		bounds = self.font.get_rect(self.text, size=self.style['size'], style=self.style.get('style', pygame.freetype.STYLE_DEFAULT))#, rotation=self.style.get('rotation', 0))
		img = pygame.Surface((bounds.width, self.font.get_sized_height(self.style['size'])), flags=pygame.SRCALPHA)
		self.font.render_to(img, (0, self.font.get_sized_ascender(self.style['size'])-bounds.top), None, **self.style)
		return img


class TimeText(Text):
	# 显示时间的文本类
	__slots__ = ['structure', 'time']

	def __init__(self, structure: str, *args, **kwargs):
		# structure 定义显示时间的结构
		# '::'表示显示时间为00:00;
		# '::.'表示时间显示为00:00.0 (小数部分取决于小数位数)
		self.structure = structure
		super().__init__('', *args, **kwargs)

	def set_time(self, time):
		self.time = time
		self.text = ''
		point = self.structure[-1] == '.'
		if point:
			self.text = f'.{time-int(time)}'
		time = int(time)
		for i in self.structure[:-1] if point else self.structure:
			self.text = ':' + str(time%60).rjust(2, '0') + self.text
			time //= 60
		self.text = self.text[1:]
		self.update_img()

	def set_part_time(self, *args, float_part=0.0):
		# 显式地设置时间，而不用计算总和，小数部分单独指定
		# 示例的两条语句等价：
		# set_part_time(2, 30)
		# set_time(150)
		time = 0
		weight = 1
		for i in args[::-1]:
			time += i * weight
			weight *= 60
		self.set_time(time)

	def get_time(self):
		# 返回当前的设定时间
		return self.time

	def get_actrul_time(self):
		# 返回当前显示的实际时间，取决于结构
		if '.' in self.text:
			self.text, time = self.text.split('.')
			time = float(time)
		else:
			time = 0
		weight = 1
		for i in self.text.split(':')[::-1]:
			time += int(i) * weight
			weight *= 60
		return time

class IconText(Text):
	# 图标文字
	__slots__ = tuple()

	def draw_text(self):
		img = self.font.render(self.text, **self.style)[0]
		return img


class Root(fantas.Ui):
	# 只用作根节点，使用 fill 填充颜色

	def __init__(self, color, **anchor):
		self.anchor = 'center'
		self.update_flag = True
		self.widgetgroup = None
		self.color = color
		fantas.NodeBase.__init__(self)
		self.temp_img = uimanager.screen
		self.size = self.temp_img.get_size()
		self.rect = self.temp_img.get_rect(**anchor)

	def render(self, target):
		self.temp_img.fill(self.color)
		if not self.is_leaf():
			for ui in self.kidgroup:
				ui.render()


class CircleLabel(Label):
	# 圆形标签(可携带边框)
	__slots__ = tuple()

	def __init__(self, radius, bg=None, bd=0, sc=None, **anchor):
		self.radius_ = radius
		self.bg = bg
		self.bd = bd
		self.sc = sc
		self.layout_data = None
		self.update_img()
		self.temp_img = self.img
		self.anchor = 'center'
		self.angle = 0
		self.alpha = self.origin_alpha = 255
		self.update_flag = True
		self.widgetgroup = None
		fantas.NodeBase.__init__(self)
		self.size = self.origin_size = self.img.get_size()
		self.rect = self.img.get_rect(**anchor)


	def update_img(self):
		self.img = pygame.Surface((self.radius_*2,self.radius_*2), flags=pygame.SRCALPHA)
		if self.bg is not None and self.radius_ > 0:
			pygame.draw.circle(self.img, self.bg, (self.radius_,self.radius_), self.radius_)
		if self.bd > 0 and self.sc is not None:
			pygame.draw.circle(self.img, self.sc, (self.radius_,self.radius_), self.radius_, width=round(self.bd))
		self.layout()

	def set_radius(self, radius):
		self.radius_ = radius
		self.mark_update()

'''
class ChildBox(Label):
	# 内部子窗口

	def __init__(self, greedy=False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.greedy = greedy

	def handle(self, event):
		super().handle(event)
		return self.greedy

	def set_greedy(self):
		# 独享事件
		# 可用于弹出式窗口，阻止用户进行其他操作
		fantas.Widget.apply_event(self, True)

	def unset_greedy(self):
		# 取消独享事件
		fantas.Widget.cancel_event(self, True)
'''

class MessageBox(Label):
	# 消息提示弹窗
	__slots__ = ['pad', 'text', 'timer']

	def __init__(self, pad, lasttime, font, textstyle, *args, **kwargs):
		super().__init__((0,0), *args, **kwargs)
		self.pad = pad
		self.text = Text('', font, textstyle, topleft=(pad,pad))
		self.text.join(self)
		self.text.anchor = 'topleft'
		self.timer = fantas.Trigger()
		self.timer.bind_endupwith(self.leave)
		self.timer.set_trigger(lasttime)

	def load_message(self, message, force=False):
		# 加载消息
		if self.text.text != message or force:
			self.text.text = message
			self.text.update_img()
			self.set_size((self.text.rect.w+self.pad*2, self.text.rect.h+self.pad*2))

	def show(self, target=None):
		# 显示弹窗
		if target is None:
			target = uimanager.screen.root
		self.join(target)
		self.timer.launch()


class HoverMessageBox(MessageBox):
	# 悬浮提示弹窗
	__slots__ = ['alpha_in', 'alpha_out']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.timer.bind_endupwith(self.show)
		self.alpha_in = fantas.UiKeyFrame(self, 'alpha', 255, 5, uimanager.slower_curve)
		self.alpha_out = fantas.UiKeyFrame(self, 'alpha', 0, 10, uimanager.slower_curve)
		self.alpha_out.bind_endupwith(self.leave)
		self.alpha = 0

	def show(self, target=None):
		if self.father is None:
			if target is None:
				target = uimanager.root
			self.join(target)
		self.alpha_in.launch('continue')

	def hide(self):
		if self.alpha_in.is_launched():
			self.alpha_in.stop()
		self.alpha_out.launch('continue')

	def set_pos(self, pos):
		self.rect.topleft = pos
		if self.rect.right > uimanager.size[0]:
			self.rect.right = uimanager.size[0]
		elif self.rect.bottom > uimanager.size[1]:
			self.rect.bottom = uimanager.size[1]

class SlideBlock(Label):
	# 单选滑块
	__slots__ = ['xy', 'options', 'options_widget', 'scale_slide', 'move_slide', 'last_option']

	def __init__(self, xy, options, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.last_option = None
		self.xy = xy
		self.options = options
		self.options_widget = []
		for i in options:
			w = fantas.AnyButton(i)
			w.bind(self.choose_, i)
			w.apply_event()
			self.options_widget.append(w)
		self.move_slide = fantas.RectKeyFrame(self, f'center{xy}', None, 15, u.harmonic_curve)

	def choose_(self, option):
		# 选中后动画
		if option is not self.last_option and not self.move_slide.is_launched():
			self.move_slide.value = getattr(option.rect, f'center{self.xy}')
			self.move_slide.launch()
			self.choose(option)
			self.last_option = option

	def choose(self, option):
		# 选中选项后执行的操作，在子类里定义
		pass
