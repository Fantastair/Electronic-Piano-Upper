import pygame
import fantas
from fantas import u


class KeyFrame:
    # 关键帧基类，提供了自动插值方法
    # 由子类定义如何利用自动插值的数据
    # 也可以用作实现定时触发函数(已经封装在Trigger类里)

    __slots__ = ['curve', 'endupwith', 'args', 'kwargs', 'start', 'totalframe', 'offset', 'currentframe']

    def __init__(self, curve=u.curve):
        self.curve = curve
        self.endupwith = None
        self.currentframe = 0

    def bind_endupwith(self, func, *args, **kwargs):
        # 绑定结束动作
        self.endupwith = func
        self.args = args
        self.kwargs = kwargs

    def set_keyframe(self, start, value, totalframe, absolute=True):
        # 设置关键帧参数
        self.start = start
        self.totalframe = totalframe
        if absolute:
            if isinstance(value, (tuple, pygame.Color)):
                self.offset = fantas.tuple_operate(value, start, fantas.sub)
            else:
                self.offset = value - start
        else:
            self.offset = value

    def launch(self):
        # 启动关键帧
        self.currentframe = 0
        if self not in u.keyframe_queue:
            u.keyframe_queue.append(self)
        return self

    def stop(self):
        # 关闭关键帧（重复关闭是安全的）
        if self in u.keyframe_queue:
            u.keyframe_queue.remove(self)

    def is_launched(self):
        # 判断是否已经启动
        return self in u.keyframe_queue

    def tick(self):
        # 进入下一帧
        if self.currentframe + 1 == self.totalframe:
            u.keyframe_queue.remove(self)
            if self.endupwith is not None:
                self.endupwith(*self.args, **self.kwargs)
        self.currentframe += 1

    def transform(self):
        # 执行一次变换
        r = self.curve.calc((self.currentframe+1)/self.totalframe)
        if isinstance(self.offset, tuple):
            return fantas.tuple_operate(self.start, fantas.tuple_int_operate(self.offset, r, fantas.mul), fantas.add)
        elif isinstance(self.offset, pygame.Color):
            return pygame.Color(fantas.tuple_operate(self.start, fantas.tuple_int_operate(self.offset, r, fantas.mul), fantas.add))
        else:
            return self.start + self.offset * r


class Trigger(KeyFrame):
    # 函数触发器
    # 使用KeyFrame的记帧功能实现

    __slots__ = ['totaltime']

    def __init__(self, func = None, *args, **kwargs):
        super().__init__(None)
        if func is not None:
            self.bind_endupwith(func, *args, **kwargs)

    def launch(self, time=None):
        # 启动触发器
        # time参数可临时指定触发时间
        if time is None:
            self.totalframe = self.totaltime
        else:
            self.totalframe = time
        super().launch()
        return self


class CircleTrigger(Trigger):
    # 循环函数触发器
    # 可以定时连续触发函数

    def __init__(self, func=None, *args, **kwargs):
        super().__init__(func, *args, **kwargs)
        self.circle_time = -1    # 表示循环触发次数，-1 代表一直循环，0 代表不循环

    def set_circle_time(self, t):
        self.circle_time = t
    
    def tick(self):
        # 进入下一帧
        self.currentframe += 1
        if self.currentframe == self.totalframe + 1:
            if self.circle_time == 0:
                u.keyframe_queue.remove(self)
            elif self.circle_time == -1:
                self.currentframe = 0
            elif self.circle_time > 0:
                self.circle_time -= 1
                self.currentframe = 0
            if self.endupwith is not None:
                self.endupwith(*self.args, **self.kwargs)
    
class AttrKeyFrame(KeyFrame):
    # 属性赋值型关键帧
    # 可以自动获取起始值

    __slots__ = ['subject', 'attr', 'value', 'absolute']

    def __init__(self, subject, attr, value, totalframe, curve, absolute=True):
        self.subject = subject
        self.attr = attr
        self.value = value
        self.totalframe = totalframe
        self.absolute = absolute
        super().__init__(curve)

    def tick(self):
        setattr(self.subject, self.attr, self.transform())
        super().tick()

    def launch(self, flag='nothing', start=None):
        # 启动关键帧
        if self.is_launched():
            if flag == 'restart':  # 重新开始
                self.currentframe = 0
            elif flag == 'continue':  # 从此开始
                if start is None:
                    start = getattr(self.subject, self.attr)
                self.set_keyframe(start, self.value, self.totalframe, self.absolute)
                self.currentframe = 0
        else:
            if flag != 'recover':
                self.currentframe = 0
            if start is None:
                start = getattr(self.subject, self.attr)
            self.set_keyframe(start, self.value, self.totalframe, self.absolute)
            u.keyframe_queue.append(self)
        return self

class UiKeyFrame(AttrKeyFrame):
    # 控制<Ui>对象的size、angle、alpha属性
    # 特别地，对于<FrameAnimation>对象，可以控制其currentframe属性实现帧动画

    __slots__ = []

    def tick(self):
        super().tick()
        self.subject.mark_update()

class UiSizeKeyFrame(UiKeyFrame):
    __slots__ = ['xy']

    def __init__(self, ui, xy, *args, **kwargs):
        self.xy = xy
        super().__init__(ui, 'size', *args, **kwargs)

    def tick(self):
        xy = self.transform()
        if self.xy == 'x':
            self.subject.size = (xy[0], self.subject.size[1])
        else:
            self.subject.size = (self.subject.size[0], xy[1])
        KeyFrame.tick(self)
        self.subject.mark_update()


class RectKeyFrame(AttrKeyFrame):
    # 控制<Ui>对象的rect的位置

    __slots__ = ['ui']

    def __init__(self, ui, *args, **kwargs):
        self.ui = ui
        super().__init__(ui.rect, *args, **kwargs)

    def tick(self):
        super().tick()
        if not self.ui.is_root():
            self.ui.father.mark_update()


class LabelKeyFrame(AttrKeyFrame):
    # 控制<Label>对象的set系列方法实现动画

    def __init__(self, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)

    def tick(self):
        getattr(self.subject, f'set_{self.attr}')(self.transform())
        self.subject.update_rect()
        KeyFrame.tick(self)


class TextKeyFrame(KeyFrame):
    # 控制<Text>对象的样式
    __slots__ = ['text', 'style', 'value', 'absolute']

    def __init__(self, text, style, value, totalframe, curve, absolute=True):
        self.text = text
        self.style = style
        self.value = value
        self.totalframe = totalframe
        self.absolute = absolute
        super().__init__(curve)

    def tick(self):
        self.text.style[self.style] = self.transform() if self.style != 'rotation' else round(self.transform())
        self.text.update_img()
        super().tick()

    def launch(self, flag=None, start=None):
        if self.is_launched():
            if flag == 'restart':
                self.currentframe = 0
            elif flag == 'continue':
                if start is None:
                    start = self.text.style[self.style]
                self.set_keyframe(start, self.value, self.totalframe, self.absolute)
                self.currentframe = 0
        else:
            self.currentframe = 0
            if start is None:
                start = self.text.style[self.style]
            self.set_keyframe(start, self.value, self.totalframe, self.absolute)
            u.keyframe_queue.append(self)
        return self

# class TimeTextKeyFrame(AttrKeyFrame):
#     # 控制时间文本显示的关键帧
#     __slots__ = []

#     def tick(self):
#         self.subject.set_time(self.subject.time)
#         super().tick()


# class MutiLabelKeyFrame(LabelKeyFrame):
#     # 一个关键帧同时可以控制多个Label对象的相同属性
#     # 一般不用于位置属性
#     __slots__ = ('label_group', 'append', 'insert', 'remove', 'pop', 'index')

#     def __init__(self, label_group=[], *args, **kwargs):
#         self.label_group = label_group
#         super().__init__(self.label_group[0], *args, **kwargs)
#         self.append = self.label_group.append
#         self.insert = self.label_group.insert
#         self.remove = self.label_group.remove
#         self.pop = self.label_group.pop
#         self.index = self.label_group.index

#     def tick(self):
#         t = self.transform()
#         for i in self.label_group:
#             getattr(i, f'set_{self.attr}')(t)
#         KeyFrame.tick(self)


# class TimeTicker:
#     # 控制时间文本用于计时
#     __slots__ = ('timetext', 'weight', 'end', 'trigger', 'start', 'start_ms', 'trigger_point')

#     def __init__(self, timetext, weight=1, end=None):
#         self.timetext = timetext
#         self.weight = weight
#         self.end = end
#         self.trigger = []

#     def launch(self, flag=None, start=None):
#         if self not in u.keyframe_queue:
#             u.keyframe_queue.append(self)
#         if start is None:
#             if flag == 'continue':
#                 self.start = self.timetext.get_time()
#             else:
#                 self.start = 0
#         else:
#             self.start = start
#         self.start_ms = pygame.time.get_ticks()
#         self.trigger_point = 0
#         return self

#     def is_launched(self):
#         return self in u.keyframe_queue

#     def stop(self):
#         if self in u.keyframe_queue:
#             u.keyframe_queue.remove(self)

#     def set_end(self, end):
#         self.end = end

#     def tick(self):
#         seconds = self.start + (pygame.time.get_ticks() - self.start_ms) / 1000 * self.weight
#         self.timetext.set_time(seconds)
#         if self.trigger:
#             for i in range(len(self.trigger[self.trigger_point:])):
#                 t = self.trigger[i]
#                 if t[0]*self.wetght <= seconds*self.wetght:
#                     t[1](*t[2], **t[3])
#                     self.trigger_point = i + 1
#                     break
#         if self.end is not None and self.weight > 0 and seconds >= self.end:
#             self.stop()

#     def set_trigger(self, sec, func, *args, **kwargs):
#         for i in range(len(self.trigger)):
#             if sec*self.weight > self.trigger[i][0]*self.weight:
#                 self.trigger.insert(i, (sec, func, args, kwargs))
#                 return
#             elif sec == self.trigger[i][0]:
#                 self.trigger[i] = (sec, func, args, kwargs)
#                 return
#         self.trigger.append((sec, func, args, kwargs))

#     def remove_trigger(self, sec):
#         for i in self.trigger:
#             if sec == i[0]:
#                 self.trigger.remove(i)
#                 return


# class BezierRectKeyFrame(KeyFrame):
#     # 通过贝塞尔曲线控制位置运动
#     __slots__ = ('ui', 'attr')

#     def __init__(self, ui, attr, totalframe, curve):
#         super().__init__(curve)
#         self.ui = ui
#         self.attr = attr
#         self.totalframe = totalframe
#         self.currentframe = 0

#     def launch(self, flag=None):
#         super().launch()
#         if flag is None:
#             self.currentframe = 0
#         return self

#     def tick(self):
#         setattr(self.ui.rect, self.attr, self.curve.calc(self.currentframe / self.totalframe))
#         self.ui.father.mark_update()
#         super().tick()
