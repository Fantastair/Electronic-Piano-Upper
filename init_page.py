import fantas
from fantas import uimanager as u
from style import *

import my_serial

root = fantas.Root(FAKEWHITE)

icon = fantas.Ui(u.images['icon'], center=(u.WIDTH // 2, u.HEIGHT // 2))
icon.size = (0, 0)
icon.alpha = 0
icon_alpha_kf = fantas.UiKeyFrame(icon, 'alpha', 255, 8, u.curve)
icon_size_kf = fantas.UiKeyFrame(icon, 'size', (256, 256), 40, fantas.SuperCurve((fantas.FormulaCurve('25*x**2'), fantas.FormulaCurve('1+math.sqrt(0.1616 - (x - 0.6)**2)')), (0, 0.2)))

stm32_box = fantas.Label((200, 200), 12, FAKEWHITE, DEEPBLUE, {'border_radius': 100}, center=(u.WIDTH // 2, u.HEIGHT // 2))
stm32_box_radius_kf = fantas.LabelKeyFrame(stm32_box, 'radius', 16, 15, u.faster_curve)
stm32_box_shake_kf = fantas.RectKeyFrame(stm32_box, 'centerx', u.WIDTH // 2 + 20, 24, fantas.SuperCurve((fantas.FormulaCurve('0.5-0.5*math.cos(4*math.pi*x)'), fantas.FormulaCurve('-math.sin(6*math.pi*x)'), fantas.FormulaCurve('0.5*math.cos(4*math.pi*x)-0.5')), (0, 0.25, 0.75)))
stm32_box_color_kf = fantas.LabelKeyFrame(stm32_box, 'sc', LIGHTRED, 16, u.curve)

stm32_text_s = fantas.Text('S', u.fonts['shuhei'], stm32_text_style, center=(100, 100))
stm32_text_s.alpha = 0
stm32_text_s_alpha_kf = fantas.UiKeyFrame(stm32_text_s, 'alpha', 255, 8, u.curve)
stm32_text_s_pos_kf = fantas.RectKeyFrame(stm32_text_s, 'centerx', 40, 8, u.harmonic_curve)
stm32_text_s_color_kf = fantas.TextKeyFrame(stm32_text_s, 'fgcolor', LIGHTRED, 16, u.curve)

stm32_text_t = fantas.Text('T', u.fonts['shuhei'], stm32_text_style, center=(100, 100))
stm32_text_t.alpha = 0
stm32_text_t_alpha_kf = fantas.UiKeyFrame(stm32_text_t, 'alpha', 255, 8, u.curve)
stm32_text_t_pos_kf = fantas.RectKeyFrame(stm32_text_t, 'centerx', 66, 8, u.harmonic_curve)
stm32_text_t_color_kf = fantas.TextKeyFrame(stm32_text_t, 'fgcolor', LIGHTRED, 16, u.curve)

stm32_text_m = fantas.Text('M', u.fonts['shuhei'], stm32_text_style, center=(100, 100))
stm32_text_m.alpha = 0
stm32_text_m_alpha_kf = fantas.UiKeyFrame(stm32_text_m, 'alpha', 255, 8, u.curve)
stm32_text_m_color_kf = fantas.TextKeyFrame(stm32_text_m, 'fgcolor', LIGHTRED, 16, u.curve)

stm32_text_3 = fantas.Text('3', u.fonts['shuhei'], stm32_text_style, center=(100, 100))
stm32_text_3.alpha = 0
stm32_text_3_alpha_kf = fantas.UiKeyFrame(stm32_text_3, 'alpha', 255, 8, u.curve)
stm32_text_3_pos_kf = fantas.RectKeyFrame(stm32_text_3, 'centerx', 134, 8, u.harmonic_curve)
stm32_text_3_color_kf = fantas.TextKeyFrame(stm32_text_3, 'fgcolor', LIGHTRED, 16, u.curve)

stm32_text_2 = fantas.Text('2', u.fonts['shuhei'], stm32_text_style, center=(100, 100))
stm32_text_2.alpha = 0
stm32_text_2_alpha_kf = fantas.UiKeyFrame(stm32_text_2, 'alpha', 255, 8, u.curve)
stm32_text_2_pos_kf = fantas.RectKeyFrame(stm32_text_2, 'centerx', 160, 8, u.harmonic_curve)
stm32_text_2_color_kf = fantas.TextKeyFrame(stm32_text_2, 'fgcolor', LIGHTRED, 16, u.curve)

competition_text = fantas.Text('2025 山东大学寒假 STM32 系统设计大赛', u.fonts['deyi'], init_info_style, center=(400, 60))
competition_text.alpha = 0
competition_text_alpha_kf = fantas.UiKeyFrame(competition_text, 'alpha', 255, 80, u.curve)
group_text = fantas.Text('小组：不会弹琴的电阻', u.fonts['deyi'], init_info_style, center=(400, 740))
group_text.alpha = 0
group_text_alpha_kf = fantas.UiKeyFrame(group_text, 'alpha', 255, 80, u.curve)

tip_text1 = fantas.Text('连接失败', u.fonts['shuhei'], tip_text_style, center=(100, 80))
tip_text2 = fantas.Text('点击重连', u.fonts['shuhei'], tip_text_style, center=(100, 120))

def ani1():
    icon_size_kf.launch()
    icon_alpha_kf.launch()
    icon_size_kf.bind_endupwith(ani2)

def ani2():
    competition_text.join(root)
    group_text.join(root)
    competition_text_alpha_kf.launch()
    group_text_alpha_kf.launch()

    icon_alpha_kf.value = 0
    icon_alpha_kf.totalframe = 15
    icon_alpha_kf.launch()
    icon_alpha_kf.bind_endupwith(ani3)
    stm32_box.join_to(root, 0)

def ani3():
    stm32_box_radius_kf.launch()

    stm32_text_s.join(stm32_box)
    stm32_text_s_alpha_kf.launch()
    fantas.Trigger(ani4).launch(4)
    stm32_text_s_alpha_kf.bind_endupwith(ani5)

def ani4():
    stm32_text_s_pos_kf.launch()
    stm32_text_s_pos_kf.bind_endupwith(ani6)

def ani5():
    stm32_text_t.join(stm32_box)
    stm32_text_t_alpha_kf.launch()
    stm32_text_t_alpha_kf.bind_endupwith(ani7)

def ani6():
    stm32_text_t_pos_kf.launch()
    fantas.Trigger(ani10).launch(8)

def ani7():
    stm32_text_m.join(stm32_box)
    stm32_text_m_alpha_kf.launch()
    ani8()

def ani8():
    stm32_text_3.join(stm32_box)
    stm32_text_3_alpha_kf.launch()
    stm32_text_3_alpha_kf.bind_endupwith(ani10)
    fantas.Trigger(ani9).launch(4)

def ani9():
    stm32_text_3_pos_kf.launch()
    stm32_text_3_pos_kf.bind_endupwith(ani11)

def ani10():
    stm32_text_2.join(stm32_box)
    stm32_text_2_alpha_kf.launch()
    ani12()

def ani11():
    stm32_text_2_pos_kf.launch()

point1 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400-50, 400-80))
p1_pos_kf1 = fantas.RectKeyFrame(point1, 'centery', 270, 15, u.harmonic_curve)
p1_pos_kf2 = fantas.RectKeyFrame(point1, 'center', (400, 230), 20, u.harmonic_curve)
p1_pos_kf1.bind_endupwith(p1_pos_kf2.launch)
p1_pos_kf3 = fantas.RectKeyFrame(point1, 'centery', 320, 6, u.harmonic_curve)
p1_pos_kf4 = fantas.RectKeyFrame(point1, 'center', (350, 270), 8, u.harmonic_curve)
p1_pos_kf4.bind_endupwith(p1_pos_kf3.launch)
point1_ = fantas.CircleLabel(8, DEEPBLUE, center=(400-50, 400-80))
p1_pos_kf1_ = fantas.RectKeyFrame(point1_, 'centery', 270, 15, u.harmonic_curve)
p1_pos_kf2_ = fantas.RectKeyFrame(point1_, 'center', (400, 230), 20, u.harmonic_curve)
p1_pos_kf1_.bind_endupwith(p1_pos_kf2_.launch)
point1__ = fantas.CircleLabel(12, FAKEWHITE, center=(400-50, 400-80))
p1_pos_kf3_ = fantas.RectKeyFrame(point1__, 'centery', 320, 6, u.harmonic_curve)
p1_pos_kf4_ = fantas.RectKeyFrame(point1__, 'center', (350, 270), 8, u.harmonic_curve)
p1_pos_kf4_.bind_endupwith(p1_pos_kf3_.launch)

point2 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400, 400-80))
p2_pos_kf = fantas.RectKeyFrame(point2, 'centery', 270, 15, u.harmonic_curve)
_p2_pos_kf = fantas.RectKeyFrame(point2, 'centery', 320, 6, u.harmonic_curve)
point2_ = fantas.CircleLabel(8, DEEPBLUE, center=(400, 400-80))
p2_pos_kf_ = fantas.RectKeyFrame(point2_, 'centery', 270, 15, u.harmonic_curve)
point2__ = fantas.CircleLabel(12, FAKEWHITE, center=(400, 400-80))
_p2_pos_kf_ = fantas.RectKeyFrame(point2__, 'centery', 320, 6, u.harmonic_curve)

point3 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400+50, 400-80))
p3_pos_kf1 = fantas.RectKeyFrame(point3, 'centery', 230, 30, u.harmonic_curve)
p3_pos_kf2 = fantas.RectKeyFrame(point3, 'center', (400, 190), 20, u.harmonic_curve)
p3_pos_kf1.bind_endupwith(p3_pos_kf2.launch)
p3_pos_kf3 = fantas.RectKeyFrame(point3, 'centery', 320, 12, u.harmonic_curve)
p3_pos_kf4 = fantas.RectKeyFrame(point3, 'center', (450, 230), 8, u.harmonic_curve)
p3_pos_kf4.bind_endupwith(p3_pos_kf3.launch)
point3_ = fantas.CircleLabel(8, DEEPBLUE, center=(400+50, 400-80))
p3_pos_kf1_ = fantas.RectKeyFrame(point3_, 'centery', 230, 30, u.harmonic_curve)
p3_pos_kf2_ = fantas.RectKeyFrame(point3_, 'center', (400, 190), 20, u.harmonic_curve)
p3_pos_kf1_.bind_endupwith(p3_pos_kf2_.launch)
point3__ = fantas.CircleLabel(12, FAKEWHITE, center=(400+50, 400-80))
p3_pos_kf3_ = fantas.RectKeyFrame(point3__, 'centery', 320, 12, u.harmonic_curve)
p3_pos_kf4_ = fantas.RectKeyFrame(point3__, 'center', (450, 230), 8, u.harmonic_curve)
p3_pos_kf4_.bind_endupwith(p3_pos_kf3_.launch)

point4 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400+80, 400-50))
p4_pos_kf1 = fantas.RectKeyFrame(point4, 'centerx', 570, 30, u.harmonic_curve)
p4_pos_kf2 = fantas.RectKeyFrame(point4, 'center', (610, 310), 20, u.harmonic_curve)
p4_pos_kf1.bind_endupwith(p4_pos_kf2.launch)
p4_pos_kf3 = fantas.RectKeyFrame(point4, 'centerx', 480, 12, u.harmonic_curve)
p4_pos_kf4 = fantas.RectKeyFrame(point4, 'center', (570, 350), 8, u.harmonic_curve)
p4_pos_kf4.bind_endupwith(p4_pos_kf3.launch)
point4_ = fantas.CircleLabel(8, DEEPBLUE, center=(400+80, 400-50))
p4_pos_kf1_ = fantas.RectKeyFrame(point4_, 'centerx', 570, 30, u.harmonic_curve)
p4_pos_kf2_ = fantas.RectKeyFrame(point4_, 'center', (610, 310), 20, u.harmonic_curve)
p4_pos_kf1_.bind_endupwith(p4_pos_kf2_.launch)
point4__ = fantas.CircleLabel(12, FAKEWHITE, center=(400+80, 400-50))
p4_pos_kf3_ = fantas.RectKeyFrame(point4__, 'centerx', 480, 12, u.harmonic_curve)
p4_pos_kf4_ = fantas.RectKeyFrame(point4__, 'center', (570, 350), 8, u.harmonic_curve)
p4_pos_kf4_.bind_endupwith(p4_pos_kf3_.launch)

point5 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400+80, 400))
p5_pos_kf = fantas.RectKeyFrame(point5, 'centerx', 570, 30, u.harmonic_curve)
_p5_pos_kf = fantas.RectKeyFrame(point5, 'centerx', 480, 12, u.harmonic_curve)
point5_ = fantas.CircleLabel(8, DEEPBLUE, center=(400+80, 400))
p5_pos_kf_ = fantas.RectKeyFrame(point5_, 'centerx', 570, 30, u.harmonic_curve)
point5__ = fantas.CircleLabel(12, FAKEWHITE, center=(400+80, 400))
_p5_pos_kf_ = fantas.RectKeyFrame(point5__, 'centerx', 480, 12, u.harmonic_curve)

point6 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400+80, 400+50))
p6_pos_kf = fantas.RectKeyFrame(point6, 'centerx', 530, 15, u.harmonic_curve)
_p6_pos_kf = fantas.RectKeyFrame(point6, 'centerx', 480, 6, u.harmonic_curve)
point6_ = fantas.CircleLabel(8, DEEPBLUE, center=(400+80, 400+50))
p6_pos_kf_ = fantas.RectKeyFrame(point6_, 'centerx', 530, 15, u.harmonic_curve)
point6__ = fantas.CircleLabel(12, FAKEWHITE, center=(400+80, 400+50))
_p6_pos_kf_ = fantas.RectKeyFrame(point6__, 'centerx', 480, 6, u.harmonic_curve)

point7 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400+50, 400+80))
p7_pos_kf1 = fantas.RectKeyFrame(point7, 'centery', 570, 30, u.harmonic_curve)
p7_pos_kf2 = fantas.RectKeyFrame(point7, 'center', (490, 610), 20, u.harmonic_curve)
p7_pos_kf1.bind_endupwith(p7_pos_kf2.launch)
p7_pos_kf3 = fantas.RectKeyFrame(point7, 'centery', 480, 12, u.harmonic_curve)
p7_pos_kf4 = fantas.RectKeyFrame(point7, 'center', (450, 570), 8, u.harmonic_curve)
p7_pos_kf4.bind_endupwith(p7_pos_kf3.launch)
point7_ = fantas.CircleLabel(8, DEEPBLUE, center=(400+50, 400+80))
p7_pos_kf1_ = fantas.RectKeyFrame(point7_, 'centery', 570, 30, u.harmonic_curve)
p7_pos_kf2_ = fantas.RectKeyFrame(point7_, 'center', (490, 610), 20, u.harmonic_curve)
p7_pos_kf1_.bind_endupwith(p7_pos_kf2_.launch)
point7__ = fantas.CircleLabel(12, FAKEWHITE, center=(400+50, 400+80))
p7_pos_kf3_ = fantas.RectKeyFrame(point7__, 'centery', 480, 12, u.harmonic_curve)
p7_pos_kf4_ = fantas.RectKeyFrame(point7__, 'center', (450, 570), 8, u.harmonic_curve)
p7_pos_kf4_.bind_endupwith(p7_pos_kf3_.launch)

point8 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400, 400+80))
p8_pos_kf = fantas.RectKeyFrame(point8, 'centery', 530, 15, u.harmonic_curve)
_p8_pos_kf = fantas.RectKeyFrame(point8, 'centery', 480, 6, u.harmonic_curve)
point8_ = fantas.CircleLabel(8, DEEPBLUE, center=(400, 400+80))
p8_pos_kf_ = fantas.RectKeyFrame(point8_, 'centery', 530, 15, u.harmonic_curve)
point8__ = fantas.CircleLabel(12, FAKEWHITE, center=(400, 400+80))
_p8_pos_kf_ = fantas.RectKeyFrame(point8__, 'centery', 480, 6, u.harmonic_curve)

point9 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400-50, 400+80))
p9_pos_kf1 = fantas.RectKeyFrame(point9, 'centery', 530, 15, u.harmonic_curve)
p9_pos_kf2 = fantas.RectKeyFrame(point9, 'center', (400, 570), 20, u.harmonic_curve)
p9_pos_kf1.bind_endupwith(p9_pos_kf2.launch)
p9_pos_kf3 = fantas.RectKeyFrame(point9, 'centery', 480, 6, u.harmonic_curve)
p9_pos_kf4 = fantas.RectKeyFrame(point9, 'center', (350, 530), 8, u.harmonic_curve)
p9_pos_kf4.bind_endupwith(p9_pos_kf3.launch)
point9_ = fantas.CircleLabel(8, DEEPBLUE, center=(400-50, 400+80))
p9_pos_kf1_ = fantas.RectKeyFrame(point9_, 'centery', 530, 15, u.harmonic_curve)
p9_pos_kf2_ = fantas.RectKeyFrame(point9_, 'center', (400, 570), 20, u.harmonic_curve)
p9_pos_kf1_.bind_endupwith(p9_pos_kf2_.launch)
point9__ = fantas.CircleLabel(12, FAKEWHITE, center=(400-50, 400+80))
p9_pos_kf3_ = fantas.RectKeyFrame(point9__, 'centery', 480, 6, u.harmonic_curve)
p9_pos_kf4_ = fantas.RectKeyFrame(point9__, 'center', (350, 530), 8, u.harmonic_curve)
p9_pos_kf4_.bind_endupwith(p9_pos_kf3_.launch)

point10 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400-80, 400+50))
p10_pos_kf1 = fantas.RectKeyFrame(point10, 'centerx', 230, 30, u.harmonic_curve)
p10_pos_kf2 = fantas.RectKeyFrame(point10, 'center', (190, 490), 20, u.harmonic_curve)
p10_pos_kf1.bind_endupwith(p10_pos_kf2.launch)
p10_pos_kf3 = fantas.RectKeyFrame(point10, 'centerx', 320, 12, u.harmonic_curve)
p10_pos_kf4 = fantas.RectKeyFrame(point10, 'center', (230, 450), 8, u.harmonic_curve)
p10_pos_kf4.bind_endupwith(p10_pos_kf3.launch)
point10_ = fantas.CircleLabel(8, DEEPBLUE, center=(400-80, 400+50))
p10_pos_kf1_ = fantas.RectKeyFrame(point10_, 'centerx', 230, 30, u.harmonic_curve)
p10_pos_kf2_ = fantas.RectKeyFrame(point10_, 'center', (190, 490), 20, u.harmonic_curve)
p10_pos_kf1_.bind_endupwith(p10_pos_kf2_.launch)
point10__ = fantas.CircleLabel(12, FAKEWHITE, center=(400-80, 400+50))
p10_pos_kf3_ = fantas.RectKeyFrame(point10__, 'centerx', 320, 12, u.harmonic_curve)
p10_pos_kf4_ = fantas.RectKeyFrame(point10__, 'center', (230, 450), 8, u.harmonic_curve)
p10_pos_kf4_.bind_endupwith(p10_pos_kf3_.launch)

point11 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400-80, 400))
p11_pos_kf = fantas.RectKeyFrame(point11, 'centerx', 190, 45, u.harmonic_curve)
_p11_pos_kf = fantas.RectKeyFrame(point11, 'centerx', 320, 18, u.harmonic_curve)
point11_ = fantas.CircleLabel(8, DEEPBLUE, center=(400-80, 400))
p11_pos_kf_ = fantas.RectKeyFrame(point11_, 'centerx', 190, 45, u.harmonic_curve)
point11__ = fantas.CircleLabel(12, FAKEWHITE, center=(400-80, 400))
_p11_pos_kf_ = fantas.RectKeyFrame(point11__, 'centerx', 320, 18, u.harmonic_curve)

point12 = fantas.CircleLabel(16, LIGHTBLUE, 8, DEEPBLUE, center=(400-80, 400-50))
p12_pos_kf1 = fantas.RectKeyFrame(point12, 'centerx', 270, 15, u.harmonic_curve)
p12_pos_kf2 = fantas.RectKeyFrame(point12, 'center', (230, 310), 20, u.harmonic_curve)
p12_pos_kf1.bind_endupwith(p12_pos_kf2.launch)
p12_pos_kf3 = fantas.RectKeyFrame(point12, 'centerx', 320, 6, u.harmonic_curve)
p12_pos_kf4 = fantas.RectKeyFrame(point12, 'center', (270, 350), 8, u.harmonic_curve)
p12_pos_kf4.bind_endupwith(p12_pos_kf3.launch)
point12_ = fantas.CircleLabel(8, DEEPBLUE, center=(400-80, 400-50))
p12_pos_kf1_ = fantas.RectKeyFrame(point12_, 'centerx', 270, 15, u.harmonic_curve)
p12_pos_kf2_ = fantas.RectKeyFrame(point12_, 'center', (230, 310), 20, u.harmonic_curve)
p12_pos_kf1_.bind_endupwith(p12_pos_kf2_.launch)
point12__ = fantas.CircleLabel(12, FAKEWHITE, center=(400-80, 400-50))
p12_pos_kf3_ = fantas.RectKeyFrame(point12__, 'centerx', 320, 6, u.harmonic_curve)
p12_pos_kf4_ = fantas.RectKeyFrame(point12__, 'center', (270, 350), 8, u.harmonic_curve)
p12_pos_kf4_.bind_endupwith(p12_pos_kf3_.launch)

class MaintainCanvas(fantas.Label):
    def __init__(self):
        super().__init__(u.size, topleft=(0, 0))

    def render(self):
        for ui in self.kidgroup:
            ui.render()
        self.father.temp_img.blit(self.temp_img, self.rect)

line_canvas = MaintainCanvas()

def ani12():
    global wait_connet
    wait_connet = False
    
    stm32_box_color_kf.value = stm32_text_s_color_kf.value = stm32_text_t_color_kf.value = stm32_text_m_color_kf.value = stm32_text_3_color_kf.value = stm32_text_2_color_kf.value = DEEPBLUE
    stm32_box_color_kf.launch()
    stm32_text_s_color_kf.launch()
    stm32_text_t_color_kf.launch()
    stm32_text_m_color_kf.launch()
    stm32_text_3_color_kf.launch()
    stm32_text_2_color_kf.launch()

    point1.join_to(root, 0)
    point2.join_to(root, 0)
    point3.join_to(root, 0)
    point4.join_to(root, 0)
    point5.join_to(root, 0)
    point6.join_to(root, 0)
    point7.join_to(root, 0)
    point8.join_to(root, 0)
    point9.join_to(root, 0)
    point10.join_to(root, 0)
    point11.join_to(root, 0)
    point12.join_to(root, 0)
    point1.rect.center = (400-50, 400-80)
    point2.rect.center = (400, 400-80)
    point3.rect.center = (400+50, 400-80)
    point4.rect.center = (400+80, 400-50)
    point5.rect.center = (400+80, 400)
    point6.rect.center = (400+80, 400+50)
    point7.rect.center = (400+50, 400+80)
    point8.rect.center = (400, 400+80)
    point9.rect.center = (400-50, 400+80)
    point10.rect.center = (400-80, 400+50)
    point11.rect.center = (400-80, 400)
    point12.rect.center = (400-80, 400-50)
    p1_pos_kf1.launch()
    p2_pos_kf.launch()
    p3_pos_kf1.launch()
    p4_pos_kf1.launch()
    p5_pos_kf.launch()
    p6_pos_kf.launch()
    p7_pos_kf1.launch()
    p8_pos_kf.launch()
    p9_pos_kf1.launch()
    p10_pos_kf1.launch()
    p11_pos_kf.launch()
    p12_pos_kf1.launch()

    line_canvas.join_to(root, 0)
    line_canvas.update_img()
    point1_.join_to(line_canvas, 0)
    point2_.join_to(line_canvas, 0)
    point3_.join_to(line_canvas, 0)
    point4_.join_to(line_canvas, 0)
    point5_.join_to(line_canvas, 0)
    point6_.join_to(line_canvas, 0)
    point7_.join_to(line_canvas, 0)
    point8_.join_to(line_canvas, 0)
    point9_.join_to(line_canvas, 0)
    point10_.join_to(line_canvas, 0)
    point11_.join_to(line_canvas, 0)
    point12_.join_to(line_canvas, 0)
    point1_.rect.center = point1.rect.center
    point2_.rect.center = point2.rect.center
    point3_.rect.center = point3.rect.center
    point4_.rect.center = point4.rect.center
    point5_.rect.center = point5.rect.center
    point6_.rect.center = point6.rect.center
    point7_.rect.center = point7.rect.center
    point8_.rect.center = point8.rect.center
    point9_.rect.center = point9.rect.center
    point10_.rect.center = point10.rect.center
    point11_.rect.center = point11.rect.center
    point12_.rect.center = point12.rect.center
    p1_pos_kf1_.launch()
    p2_pos_kf_.launch()
    p3_pos_kf1_.launch()
    p4_pos_kf1_.launch()
    p5_pos_kf_.launch()
    p6_pos_kf_.launch()
    p7_pos_kf1_.launch()
    p8_pos_kf_.launch()
    p9_pos_kf1_.launch()
    p10_pos_kf1_.launch()
    p11_pos_kf_.launch()
    p12_pos_kf1_.launch()

    p10_pos_kf2.bind_endupwith(check_serial)

class STM32BoxMouseWidget(fantas.MouseBase):
    def __init__(self):
        super().__init__(stm32_box, 2)
    
    def mousein(self):
        if wait_connet:
            stm32_text_s.leave()
            stm32_text_t.leave()
            stm32_text_m.leave()
            stm32_text_3.leave()
            stm32_text_2.leave()
            tip_text1.join(stm32_box)
            tip_text2.join(stm32_box)
    
    def mouseout(self):
        stm32_text_s.join(stm32_box)
        stm32_text_t.join(stm32_box)
        stm32_text_m.join(stm32_box)
        stm32_text_3.join(stm32_box)
        stm32_text_2.join(stm32_box)
        tip_text1.leave()
        tip_text2.leave()
    
    def mouseclick(self):
        if wait_connet:
            ani12()
            self.mouseout()
    
    def handle(self, event):
        super().handle(event)
        if event.type == u.CONNECTEDEVENT:
            tip_text1.text = '连接成功'
            tip_text2.text = '点击继续'
            tip_text1.update_img()
            tip_text2.update_img()

STM32BoxMouseWidget().apply_event()

wait_connet = False
def ani13():
    global wait_connet
    wait_connet = True

    stm32_box_shake_kf.launch()
    stm32_box_color_kf.value = stm32_text_s_color_kf.value = stm32_text_t_color_kf.value = stm32_text_m_color_kf.value = stm32_text_3_color_kf.value = stm32_text_2_color_kf.value = LIGHTRED
    stm32_box_color_kf.launch()
    stm32_text_s_color_kf.launch()
    stm32_text_t_color_kf.launch()
    stm32_text_m_color_kf.launch()
    stm32_text_3_color_kf.launch()
    stm32_text_2_color_kf.launch()

    p1_pos_kf4.launch()
    _p2_pos_kf.launch()
    p3_pos_kf4.launch()
    p4_pos_kf4.launch()
    _p5_pos_kf.launch()
    _p6_pos_kf.launch()
    p7_pos_kf4.launch()
    _p8_pos_kf.launch()
    p9_pos_kf4.launch()
    p10_pos_kf4.launch()
    _p11_pos_kf.launch()
    p12_pos_kf4.launch()

    point1_.leave()
    point2_.leave()
    point3_.leave()
    point4_.leave()
    point5_.leave()
    point6_.leave()
    point7_.leave()
    point8_.leave()
    point9_.leave()
    point10_.leave()
    point11_.leave()
    point12_.leave()

    point1__.join(line_canvas)
    point2__.join(line_canvas)
    point3__.join(line_canvas)
    point4__.join(line_canvas)
    point5__.join(line_canvas)
    point6__.join(line_canvas)
    point7__.join(line_canvas)
    point8__.join(line_canvas)
    point9__.join(line_canvas)
    point10__.join(line_canvas)
    point11__.join(line_canvas)
    point12__.join(line_canvas)

    point1__.rect.center = point1.rect.center
    point2__.rect.center = point2.rect.center
    point3__.rect.center = point3.rect.center
    point4__.rect.center = point4.rect.center
    point5__.rect.center = point5.rect.center
    point6__.rect.center = point6.rect.center
    point7__.rect.center = point7.rect.center
    point8__.rect.center = point8.rect.center
    point9__.rect.center = point9.rect.center
    point10__.rect.center = point10.rect.center
    point11__.rect.center = point11.rect.center
    point12__.rect.center = point12.rect.center

    p1_pos_kf4_.launch()
    _p2_pos_kf_.launch()
    p3_pos_kf4_.launch()
    p4_pos_kf4_.launch()
    _p5_pos_kf_.launch()
    _p6_pos_kf_.launch()
    p7_pos_kf4_.launch()
    _p8_pos_kf_.launch()
    p9_pos_kf4_.launch()
    p10_pos_kf4_.launch()
    _p11_pos_kf_.launch()
    p12_pos_kf4_.launch()

def check_serial():
    if my_serial.connected:
        import main_page
        u.root = main_page.root
        main_page.ani1()
    else:
        ani13()

def start():
    u.root = root
    icon.join(root)
    fantas.Trigger(ani1).launch(15)
