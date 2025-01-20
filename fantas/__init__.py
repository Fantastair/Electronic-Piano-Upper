from .resource import *
from .abstract import *
from .framework import *

# 预设曲线
# y = x
uimanager.curve = Curve()
# 渐快(加速)
uimanager.faster_curve = FormulaCurve('x**2')
# 渐慢(刹车/弹射)
uimanager.slower_curve = FormulaCurve('2*x-x**2')
# 简谐(平滑/惯性)(本应用正弦函数，但是发现一条高度重合的三次曲线，计算速度稍快)
# 原正弦函数：(1-math.cos(math.pi*x))/2
uimanager.harmonic_curve = FormulaCurve('3*x**2-2*x**3')
# 正弦(抖动/原地)
uimanager.sin_curve = FormulaCurve('math.sin(math.pi*x*2)')
# 抛物线(最高点1)
# uimanager.parabola1 = FormulaCurve('4*x-4*x**2')
# 越界回弹线
uimanager.rebound_curve = FormulaCurve('-2*x**2+3*x')
# 尺寸回转线
# uimanager.cos_curve = FormulaCurve('math.cos(math.pi*x*3)/2+0.5')

from .basicui import *
from .basicwidget import *
from .keyframe import *
from .uiwidget import *
