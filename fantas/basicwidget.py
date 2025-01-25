import pygame
from .framework import Widget, uimanager


class MouseBase(Widget):
    # 鼠标事件抽象基类

    __slots__ = ['level', 'mousedown', 'events', 'mouseon', 'methods']

    def __init__(self, ui, level=1):
        super().__init__(ui)
        self.level = level  # 事件处理等级
        self.mousedown = None  # 标记按中的建
        if level == 1:  # 1级可以处理点击事件
            self.events = [
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.WINDOWFOCUSLOST,
            pygame.WINDOWFOCUSGAINED,
            pygame.WINDOWEXPOSED,
            pygame.WINDOWMINIMIZED,
            ]
        elif level == 2:  # 2级可以处理移动事件
            self.events = [
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
            pygame.WINDOWLEAVE,
            pygame.WINDOWENTER,
            pygame.WINDOWFOCUSLOST,
            pygame.WINDOWFOCUSGAINED,
            pygame.WINDOWEXPOSED,
            pygame.WINDOWMINIMIZED,
            ]
            self.mouseon = False
        elif level == 3:  # 3级可以处理滚轮事件
            self.events = [
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
            pygame.WINDOWLEAVE,
            pygame.WINDOWENTER,
            pygame.MOUSEWHEEL,
            pygame.WINDOWFOCUSLOST,
            pygame.WINDOWFOCUSGAINED,
            pygame.WINDOWEXPOSED,
            pygame.WINDOWMINIMIZED,
            ]
            self.mouseon = False
        self.methods = methods[:level]

    def handle(self, event):
        if event.type in self.events:
            for h in self.methods:
                h(self, event)

    def handle1(self, event):
        # 点击事件抽象
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.ui.rect.collidepoint(event.pos) and self.mousedown is None:
                self.mousedown = event.button
            self.mousepress(event.pos, event.button)  # 按下
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouserelease(event.pos, event.button)  # 释放
            if self.ui.rect.collidepoint(event.pos) and self.mousedown is not None:
                self.mouseclick()  # 有效单击
            self.mousedown = None
        elif event.type == pygame.WINDOWFOCUSLOST:
            self.window_lose_focus()  # 窗口失去焦点
        elif event.type == pygame.WINDOWFOCUSGAINED:
            self.window_gain_focus()  # 窗口获得焦点
        elif event.type == pygame.WINDOWEXPOSED:
            self.window_expose()  # 窗口暴露
        elif event.type == pygame.WINDOWMINIMIZED:
            self.window_hide()  # 窗口隐藏

    def handle2(self, event):
        # 移动事件抽象
        if event.type == pygame.MOUSEMOTION:
            if self.mouseon:
                if not self.ui.rect.collidepoint(event.pos):
                    self.mouseon = False
                    self.mouseout()  # 移出
            elif self.ui.rect.collidepoint(event.pos):
                self.mouseon = True
                self.mousein()  # 移入
            if self.mousemove is not None:
                self.mousemove(event.pos)  # 移动
        elif event.type == pygame.WINDOWLEAVE:
            self.mouse_leavewindow()  # 离开窗口
        elif event.type == pygame.WINDOWENTER:
            self.mouse_enterwindow()  # 进入窗口

    def handle3(self, event):
        # 滚轮事件抽象
        if event.type == pygame.MOUSEWHEEL:
            self.mousescroll(event.x, event.y)  # 滚轮滚动


    def mousepress(self, pos, button):
        pass

    def mouserelease(self, pos, button):
        pass

    def mouseclick(self):
        pass

    def mouseout(self):
        pass

    def mousein(self):
        pass

    def mouse_leavewindow(self):
        # 离开窗口默认触发移出动作
        if self.mouseon:
            self.mouseon = False
            self.mouseout()

    def mouse_enterwindow(self):
        pass

    mousemove = None

    def mousescroll(self, x, y):
        # x右正左负，y上正下负
        pass

    def window_lose_focus(self):
        # 窗口失去焦点
        pass

    def window_gain_focus(self):
        # 窗口获得焦点
        pass

    def window_expose(self):
        # 窗口暴露
        pass

    def window_hide(self):
        # 窗口隐藏
        pass


methods = (MouseBase.handle1, MouseBase.handle2, MouseBase.handle3)


class AnyButton(MouseBase):
    # 任意按钮，可以套在任何一个Ui上

    __slots__ = ['func', 'args', 'kwargs']

    def bind(self, func, *args, **kwargs):
        # 绑定函数
        self.func, self.args, self.kwargs = func, args, kwargs

    def mouseclick(self):
        if self.mousedown == 1:
            self.func(*self.args, **self.kwargs)


class KeyboardBase(Widget):
    # 键盘事件抽象类(不包括输入事件)
    __slots__ = []

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            self.keyboardpress(event.key, event.shortcut)  # 键盘按下 
        elif event.type == pygame.KEYUP:
            self.keyboardrelease(event.key, event.shortcut)  # 键盘释放

    def keyboardpress(self, key, shortcut):
        pass

    def keyboardrelease(self, key, shortcut):
        pass

# '''
# class TextInputBase(Widget):
#     # 文本输入事件抽象

#     __slots__ = ['inputing']

#     events = (pygame.TEXTINPUT, pygame.TEXTEDITING)
#     rect = pygame.Rect((0,0,0,0))

#     def __init__(self, ui):
#         super().__init__(ui)
#         self.inputing = False

#     def start_input(self):
#         # 开始接收输入
#         pygame.key.start_text_input()
#         left, top = self.ui.get_absolute_pos()
#         self.rect.topleft = (left, top+self.ui.rect.height)
#         pygame.key.set_text_input_rect(self.rect)
#         self.apply_event()
#         self.inputing = True

#     def stop_input(self):
#         # 停止接收输入
#         pygame.key.stop_text_input()
#         self.cancel_event()
#         self.inputing = False

#     def handle(self, event):
#         if self.inputing and event.type in self.events:
#             if event.type == pygame.TEXTINPUT:
#                 self.textinput(event.text)  # 文本输入
#             elif event.type == pygame.TEXTEDITING:
#                 self.textedit(event.text, event.start)  # 文本编辑

#     def textinput(self, text):
#         pass

#     def textedit(self, text, start):
#         # start下次输入文本的位置
#         pass
# '''
'''
class HoverMessage(MouseBase):
    # 悬浮提示弹窗组件
    # 多个组件可以共享一个<HoverMessageBox>
    __slots__ = ['text', 'messagebox']

    def __init__(self, ui, text, box):
        super().__init__(ui, 2)
        self.text = text
        self.messagebox = box

    def mousemove(self, pos):
        if self.mouseon and self.messagebox.father is None:
            self.messagebox.load_message(self.text)
            self.messagebox.set_pos(pygame.mouse.get_pos())
            self.messagebox.timer.launch()
            if self.messagebox.alpha_out.is_launched():
                self.messagebox.alpha_out.stop()

    def mouseout(self):
        if self.messagebox.timer.is_launched():
            self.messagebox.timer.stop()
        elif self.messagebox.father is not None:
            self.messagebox.hide()

    def cancel_event(self):
        super().cancel_event()
        self.mouseon = False
        self.mouseout()

# '''
