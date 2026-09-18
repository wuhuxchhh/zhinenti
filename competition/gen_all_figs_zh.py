"""
光合日程AI - 全部技术图统一生成 v2
风格：参考 page06 浅色圆角盒 + 细黑边 + 弧形箭头
字体: SimHei
字号: 中等（接近参考图比例）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import numpy as np

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['font.family'] = 'sans-serif'
rcParams['axes.unicode_minus'] = False

# ============================================================
# 全局样式（参照 page06 思维导图）
# ============================================================
# 颜色：浅粉/浅绿/浅蓝，对应参考图
C_ROOT    = '#FF8A95'   # 根节点（深粉）
C_BRANCH  = '#A8E0A0'   # 分支节点（浅绿）
C_LEAF    = '#A0D8F0'   # 叶子节点（浅蓝）
C_HW      = '#FFD8A8'   # 硬件节点（浅橙）
C_SENSOR  = '#FFB8B8'   # 传感器节点
C_FLOW    = '#D4E8B0'   # 流程节点
C_WARN    = '#FFE082'   # 警示节点

# 字号（放大：标题 22，框标题 18，正文 15，注释 12）
FS_TITLE   = 22
FS_BIG     = 18
FS_NORMAL  = 15
FS_SMALL   = 12
FS_TICK    = 12
FS_LEGEND  = 13

# 边线/箭头
EDGE_COLOR = '#222222'
ARROW_COLOR = '#444444'
EDGE_LW = 1.8
ARROW_LW = 1.4

OUT = 'C:/zhinenti/competition/figs'

# 工具函数
def style_box(ax, x, y, w, h, text, facecolor, edgecolor=EDGE_COLOR, lw=EDGE_LW, fontsize=FS_NORMAL, weight='normal', text_color='#000'):
    box = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle='round,pad=0.08', facecolor=facecolor, edgecolor=edgecolor, linewidth=lw)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight=weight, color=text_color)

def curve_arrow(ax, x1, y1, x2, y2, color=ARROW_COLOR, lw=ARROW_LW, rad=0.2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='->', color=color, lw=lw, connectionstyle=f'arc3,rad={rad}'))

def line_arrow(ax, x1, y1, x2, y2, color=ARROW_COLOR, lw=ARROW_LW):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=color, lw=lw))

# ============================================================
# FIG 1: 系统架构总览（仿参考图：三栏布局）
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 9.1))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('光合日程AI · 双MCU系统架构总览', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 根节点
style_box(ax, 1.2, 4, 2.0, 1.0, '光合日程AI\n双MCU系统', C_ROOT, fontsize=FS_BIG, weight='bold')

# 中间层
mids = [
    (4.5, 6.2, 'AI 主板\nXIAO ESP32-S3'),
    (4.5, 4.0, '板间 I2C\n6字节 @1Hz'),
    (4.5, 1.8, '显示板\nESP32-C3'),
]
for x, y, t in mids:
    style_box(ax, x, y, 2.4, 1.0, t, C_BRANCH, fontsize=FS_NORMAL, weight='bold')

# 右侧
rights = [
    (9, 6.6, 'VL53L0X\nToF 距离', C_SENSOR),
    (9, 5.0, 'TCS34725\n颜色/手势', C_SENSOR),
    (9, 3.4, 'MAX30102\n心率/血氧', C_SENSOR),
    (9, 1.8, 'WS2812\n60 LED 灯条', C_HW),
    (9.0, 0.3, 'SH1106 OLED\nDS3231 RTC', C_HW),
]

# Actually re-arrange: AI主板传感器在右列上方；显示板输出在下方
rights = [
    (9, 6.7, 'VL53L0X\nToF 距离', C_SENSOR),
    (9, 5.4, 'TCS34725\n颜色/手势', C_SENSOR),
    (9, 4.1, 'MAX30102\n心率/血氧', C_SENSOR),
    (9, 2.0, 'SH1106 OLED\nDS3231 RTC', C_HW),
    (9, 0.5, 'WS2812\n60 LED 灯条', C_HW),
]
for x, y, t, c in rights:
    style_box(ax, x, y, 2.2, 0.9, t, c, fontsize=FS_SMALL)

# 连线
curve_arrow(ax, 2.2, 4.4, 3.3, 6.0, color='#1565C0')
curve_arrow(ax, 2.2, 4.0, 3.3, 4.0, color='#666')
curve_arrow(ax, 2.2, 3.6, 3.3, 2.0, color='#2E7D32')

curve_arrow(ax, 5.7, 6.4, 7.9, 6.6, color='#1565C0')
curve_arrow(ax, 5.7, 6.0, 7.9, 5.4, color='#1565C0')
curve_arrow(ax, 5.7, 5.7, 7.9, 4.1, color='#1565C0')
curve_arrow(ax, 5.7, 1.9, 7.9, 2.0, color='#2E7D32')
curve_arrow(ax, 5.7, 1.6, 7.9, 0.5, color='#2E7D32')

ax.text(6, 0.05, '感知+处理 (AI) | 通信协议 | 显示+计时 (Display)', ha='center', fontsize=FS_SMALL, style='italic', color='#666')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_architecture.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_architecture.png saved')

# ============================================================
# FIG 2: 手势检测算法流程图
# ============================================================
fig, ax = plt.subplots(figsize=(14.0, 15.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13)
ax.axis('off')
ax.set_title('手势检测算法 · TCS34725 12 帧色彩方差分析', fontsize=FS_TITLE, fontweight='bold', pad=10)

style_box(ax, 5, 12.2, 5.5, 0.7, '采集 TCS34725 RGBC × 12 帧（间隔 ~10 ms）', C_FLOW, fontsize=FS_NORMAL, weight='bold')
line_arrow(ax, 5, 11.8, 5, 11.2)
style_box(ax, 5, 10.8, 5.5, 0.7, '计算帧间方差 total = Σ(|dR|+|dG|+|dB|+|dC|)', C_FLOW, fontsize=FS_NORMAL, weight='bold')
line_arrow(ax, 5, 10.4, 5, 9.8)
style_box(ax, 5, 9.4, 4.0, 0.7, 'total < 4000?', C_WARN, fontsize=FS_NORMAL, weight='bold')

# 分支
line_arrow(ax, 3.0, 9.4, 2.0, 8.4, color='#1B5E20')
ax.text(2.5, 8.95, '是', fontsize=FS_SMALL, color='#1B5E20', fontweight='bold')
line_arrow(ax, 7.0, 9.4, 8.0, 8.4, color='#B71C1C')
ax.text(7.5, 8.95, '否', fontsize=FS_SMALL, color='#B71C1C', fontweight='bold')

style_box(ax, 2.0, 8.0, 2.6, 0.7, '无手势 返回 -1', C_BRANCH, fontsize=FS_NORMAL, weight='bold')

style_box(ax, 8.0, 8.0, 2.6, 0.7, 'total > 12000?', C_WARN, fontsize=FS_NORMAL, weight='bold')
line_arrow(ax, 8.0, 7.65, 8.0, 7.0, color='#B71C1C')
ax.text(8.15, 7.35, '是', fontsize=FS_SMALL, color='#B71C1C', fontweight='bold')
line_arrow(ax, 8.0, 7.65, 5.0, 5.0, color='#1565C0')
ax.text(6.5, 6.2, '否 → 慢速', fontsize=FS_SMALL, color='#1565C0', fontweight='bold')

style_box(ax, 8.0, 6.5, 2.8, 0.8, '快速挥手\n800ms 内双击?', C_SENSOR, fontsize=FS_NORMAL, weight='bold')
line_arrow(ax, 8.0, 6.1, 6.3, 4.6, color='#6A1B9A')
ax.text(7.0, 5.2, '是→双击', fontsize=FS_SMALL, color='#6A1B9A', fontweight='bold')
line_arrow(ax, 8.0, 6.1, 9.3, 4.6, color='#666')
ax.text(8.9, 5.4, '否', fontsize=FS_SMALL, color='#666', fontweight='bold')

style_box(ax, 6.3, 4.2, 2.6, 0.7, '双击触发\n心率/血氧测量', C_ROOT, fontsize=FS_NORMAL, weight='bold')
style_box(ax, 9.3, 4.2, 1.4, 0.7, '丢弃', '#E0E0E0', fontsize=FS_SMALL)

# 慢速分支
style_box(ax, 5.0, 3.0, 5.5, 0.8, '慢速挥手：分析 C 通道\nc_last - c_first > 800 = 接近', C_FLOW, fontsize=FS_NORMAL, weight='bold')
line_arrow(ax, 4.0, 2.55, 3.0, 1.5, color='#1B5E20')
ax.text(3.4, 2.1, '接近', fontsize=FS_SMALL, color='#1B5E20', fontweight='bold')
line_arrow(ax, 6.0, 2.55, 7.0, 1.5, color='#B71C1C')
ax.text(6.5, 2.1, '远离', fontsize=FS_SMALL, color='#B71C1C', fontweight='bold')

style_box(ax, 3.0, 1.1, 2.2, 0.7, '接近 g=2\n亮度 +20', C_BRANCH, fontsize=FS_NORMAL, weight='bold')
style_box(ax, 7.0, 1.1, 2.2, 0.7, '远离 g=3\n亮度 -20', C_BRANCH, fontsize=FS_NORMAL, weight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_gesture_flowchart.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_gesture_flowchart.png saved')

# ============================================================
# FIG 3: 疲劳生物标志物曲线
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14.0, 9.1), sharex=True)
time = np.arange(0, 56, 5)
hr = [72, 71.5, 71, 71.3, 71.1, 71.5, 72, 71.8, 72.2, 71.3, 71, 71.5]
spo2 = [98.1, 98.0, 98.0, 98.0, 97.9, 97.8, 97.7, 97.8, 97.8, 97.7, 97.6, 97.7]
fatigue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

ax1.plot(time, hr, 'o-', color='#D32F2F', lw=2, markersize=6, label='心率 HR (bpm)')
ax1.axhline(85, color='#D32F2F', linestyle='--', lw=1, label='风险阈值 (>85)')
ax1.set_ylabel('心率 (bpm)', fontsize=FS_NORMAL, color='#D32F2F')
ax1.tick_params(axis='y', labelsize=FS_TICK)
ax1.tick_params(axis='x', labelsize=FS_TICK)
ax1.legend(loc='upper left', fontsize=FS_LEGEND)
ax1.grid(True, alpha=0.3)
ax1.set_title('疲劳生物标志物随时间变化（模拟数据）', fontsize=FS_TITLE, fontweight='bold', pad=8)

ax2.plot(time, spo2, 's-', color='#1976D2', lw=2, markersize=6, label='血氧 SpO2 (%)')
ax2.axhline(95, color='#1976D2', linestyle='--', lw=1, label='风险阈值 (<95%)')
ax2.set_ylabel('血氧 (%)', fontsize=FS_NORMAL, color='#1976D2')
ax2.set_xlabel('伏案时间 (分钟)', fontsize=FS_NORMAL)
ax2.legend(loc='upper left', fontsize=FS_LEGEND)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='y', labelsize=FS_TICK)
ax2.tick_params(axis='x', labelsize=FS_TICK)

fatigue_colors = ['#4CAF50' if f == 0 else '#FFC107' if f == 1 else '#F44336' for f in fatigue]
ax3 = ax2.twinx()
ax3.bar(time, [0.3]*len(time), bottom=94.7, color=fatigue_colors, width=2.5, alpha=0.85)
ax3.set_ylim(94.5, 98.5)
ax3.set_yticks([94.8, 95.5, 96.5])
ax3.set_yticklabels(['OK', 'Tired', 'Rest!'], fontsize=FS_TICK)
ax3.set_ylabel('疲劳等级', fontsize=FS_NORMAL, color='#555')

ax1.text(53, 84.0, '>45min 触发\n黄灯 Tired', ha='right', fontsize=FS_SMALL, color='#E65100',
         bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F57F17', pad=0.3))

plt.tight_layout()
plt.savefig(f'{OUT}/fig_fatigue_curve.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_fatigue_curve.png saved')

# ============================================================
# FIG 4: I2C 总线拓扑（仿参考图风格）
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 9.1))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('I2C 总线拓扑 · 双MCU 多角色设计', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 根
style_box(ax, 1.5, 4, 2.2, 1.0, '双MCU\nI2C 拓扑', C_ROOT, fontsize=FS_BIG, weight='bold')

# 中层
style_box(ax, 4.5, 6, 2.4, 0.9, 'AI 主板\nESP32-S3', C_BRANCH, fontsize=FS_NORMAL, weight='bold')
style_box(ax, 4.5, 2, 2.4, 0.9, '显示板\nESP32-C3', C_BRANCH, fontsize=FS_NORMAL, weight='bold')

# 板间 I2C
style_box(ax, 4.5, 4, 2.4, 0.7, '板间 6 字节 @1Hz', C_WARN, fontsize=FS_SMALL, weight='bold')
line_arrow(ax, 2.6, 4.0, 3.3, 4.0)
line_arrow(ax, 5.7, 6.0, 9.0, 6.5)
line_arrow(ax, 5.7, 2.0, 9.0, 1.5)

# AI 板外设
style_box(ax, 9.5, 6.7, 2.4, 0.6, 'I2C Bus 0 (GPIO8/9)', C_HW, fontsize=FS_SMALL)
style_box(ax, 9.5, 5.9, 1.4, 0.5, 'VL53L0X', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 9.5, 5.0, 2.4, 0.5, 'I2C Bus 1 (GPIO1/2)', C_HW, fontsize=FS_SMALL)
style_box(ax, 8.6, 4.3, 1.2, 0.4, 'TCS34725', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 10.4, 4.3, 1.2, 0.4, 'MAX30102', C_SENSOR, fontsize=FS_SMALL)

# 显示板外设
style_box(ax, 9.5, 2.7, 2.4, 0.5, '硬件 I2C 从机 (GPIO4/5)', C_HW, fontsize=FS_SMALL)
style_box(ax, 9.5, 1.9, 1.4, 0.4, 'I2C 0x08', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 9.5, 1.0, 2.4, 0.5, '软 I2C (GPIO8/9) 位带', C_HW, fontsize=FS_SMALL)
style_box(ax, 8.6, 0.3, 1.2, 0.4, 'SH1106', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 10.4, 0.3, 1.2, 0.4, 'DS3231', C_SENSOR, fontsize=FS_SMALL)

ax.text(6, 7.5, '两片 0x29 通过不同总线隔离 (VL53L0X Bus0 / TCS34725 Bus1)', ha='center', fontsize=FS_SMALL, style='italic', color='#1565C0')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_i2c_topology.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_i2c_topology.png saved')

# ============================================================
# FIG 5: 番茄钟状态机
# ============================================================
fig, ax = plt.subplots(figsize=(14.0, 9.1))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('番茄钟状态机 · 三态自动切换', fontsize=FS_TITLE, fontweight='bold', pad=10)

style_box(ax, 2, 5.5, 2.4, 1.0, 'WORK 工作\n40 分钟', '#FFD8A8', fontsize=FS_NORMAL, weight='bold')
style_box(ax, 8, 5.5, 2.4, 1.0, 'REST 休息\n5 分钟', '#A0D8F0', fontsize=FS_NORMAL, weight='bold')
style_box(ax, 5, 2, 2.4, 1.0, 'IDLE 待机', C_BRANCH, fontsize=FS_NORMAL, weight='bold')

# 转换
line_arrow(ax, 3.2, 5.5, 6.8, 5.5, color='#FF6F00', lw=1.5)
ax.text(5, 6.1, '工作 40min 到时', ha='center', fontsize=FS_SMALL, color='#E65100', fontweight='bold')
line_arrow(ax, 6.8, 5.5, 3.2, 5.5, color='#1565C0', lw=1.5)
ax.text(5, 4.9, '休息 5min 到时', ha='center', fontsize=FS_SMALL, color='#0D47A1', fontweight='bold')

curve_arrow(ax, 2, 5.0, 4, 2.5, color='#2E7D32')
ax.text(2.2, 3.7, 'I2C cmd=1\n开始', fontsize=FS_SMALL, color='#1B5E20')
curve_arrow(ax, 5, 2.5, 2.5, 5.0, color='#C62828', rad=-0.3)
ax.text(3.0, 4.0, 'I2C cmd=2\n停止', fontsize=FS_SMALL, color='#B71C1C')

ax.text(5, 0.5, '触发：定时器到期（自动） | AI主板 I2C 命令（手动）', ha='center', fontsize=FS_SMALL, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_pomodoro_state.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_pomodoro_state.png saved')

# ============================================================
# FIG 6: 姿态检测区域
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 7.7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.5)
ax.axis('off')
ax.set_title('姿态检测三区域 · VL53L0X ToF 测距', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 桌面
desk = mpatches.FancyBboxPatch((0.5, 0.5), 11, 0.9, boxstyle='round', facecolor='#F5DEB3', edgecolor='#8D6E63', linewidth=1.2)
ax.add_patch(desk)
ax.text(6, 0.95, '桌   面', ha='center', fontsize=FS_BIG, fontweight='bold', color='#5D4037')

# 人形
ax.plot([3, 3], [2.2, 4.0], 'k-', lw=2, alpha=0.7)
ax.plot([3, 2.4], [2.2, 2.8], 'k-', lw=2, alpha=0.7)
ax.plot([3, 3.6], [2.2, 2.8], 'k-', lw=2, alpha=0.7)

# 传感器
sensor = mpatches.FancyBboxPatch((5.5, 1.25), 0.8, 0.4, boxstyle='round', facecolor='#4CAF50', edgecolor='#1B5E20', linewidth=1.2)
ax.add_patch(sensor)
ax.text(5.9, 1.45, 'VL53L0X', ha='center', fontsize=FS_SMALL, color='white', fontweight='bold')

# 区域
zones = [
    (0.7, 1.8, 3.0, 0.7, '伏案 (0-400mm)\n用户坐在桌前', '#C8E6C9'),
    (4.0, 1.8, 3.0, 0.7, '靠椅 (400-700mm)\n用户后仰', '#FFF9C4'),
    (7.2, 1.8, 4.0, 0.7, '离座 (>700mm)\n用户离开', '#FFCDD2'),
]
for x, y, w, h, t, c in zones:
    style_box(ax, x+w/2, y+h/2, w, h, t, c, fontsize=FS_SMALL, weight='bold')

# LED 颜色
leds = [
    (2.2, 3.4, 'LED 暖白\n(255,220,180)', '#FFDAB4'),
    (5.5, 3.4, 'LED 冷蓝\n(180,200,255)', '#B4C8FF'),
    (9.2, 3.4, 'LED 暗灰\n(80,80,80)', '#888888'),
]
for x, y, t, c in leds:
    ax.text(x, y+0.2, t, ha='center', va='top', fontsize=FS_SMALL, color='#333')
    circle = plt.Circle((x, y-0.1), 0.12, color=c, ec='#333', linewidth=1)
    ax.add_patch(circle)

# 距离刻度
for d in range(0, 1100, 200):
    x = 0.5 + d/1000 * 11
    ax.plot([x, x], [4.6, 4.9], 'k-', lw=0.5)
    ax.text(x, 5.0, f'{d}mm', ha='center', fontsize=FS_TICK)

plt.tight_layout()
plt.savefig(f'{OUT}/fig_posture_zones.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_posture_zones.png saved')

# ============================================================
# FIG 7: 板间 I2C 通信协议
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 6.3))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title('板间 I2C 通信协议 · 6 字节定长包 @1Hz', fontsize=FS_TITLE, fontweight='bold', pad=10)

bytes_data = [
    (1.0, 2.8, 1.5, 1.2, '字节 0', '#E3F2FD', '心率', 'uint8'),
    (2.7, 2.8, 1.5, 1.2, '字节 1', '#E3F2FD', '血氧', 'uint8'),
    (4.4, 2.8, 1.5, 1.2, '字节 2', '#FFF9C4', '疲劳等级', '0-2'),
    (6.1, 2.8, 1.5, 1.2, '字节 3', '#FFF9C4', '姿态', '0-2'),
    (7.8, 2.8, 1.5, 1.2, '字节 4', '#F3E5F5', '手势', '保留'),
    (9.5, 2.8, 1.5, 1.2, '字节 5', '#F3E5F5', '番茄钟', 'cmd'),
]
for i, (x, y, w, h, hdr, c, lbl, sub) in enumerate(bytes_data):
    box = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle='round,pad=0.05', facecolor=c, edgecolor=EDGE_COLOR, linewidth=EDGE_LW)
    ax.add_patch(box)
    ax.text(x, y+0.35, hdr, ha='center', fontsize=FS_NORMAL, fontweight='bold')
    ax.text(x, y, lbl, ha='center', fontsize=FS_NORMAL, fontweight='bold')
    ax.text(x, y-0.35, sub, ha='center', fontsize=FS_TICK, color='#555')

# 帧间箭头
for i in range(5):
    x = 1.0 + (i+1) * 1.7 - 0.85
    line_arrow(ax, x, 2.8, x+0.1, 2.8, color='#D84315', lw=1.2)

ax.annotate('', xy=(10.5, 4.5), xytext=(1.5, 4.5), arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
ax.text(6, 4.7, 'ESP32-S3 (主) → ESP32-C3 (从 @0x08)', ha='center', fontsize=FS_NORMAL, color='#1565C0', fontweight='bold')

ax.text(6, 1.0, '传输：1 Hz | I2C 速率：100 kHz | 无超时（fire-and-forget）', ha='center', fontsize=FS_SMALL, style='italic', color='#666')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_data_protocol.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_data_protocol.png saved')

# ============================================================
# FIG 8: LED 色彩反馈系统
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 8.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('LED 色彩反馈系统 · 姿态 × 疲劳双通道', fontsize=FS_TITLE, fontweight='bold', pad=10)

led_states = [
    (0.7, 5.0, 2.4, 1.2, '姿态：伏案', '#FFDAB4', '暖白色\n(255,220,180)'),
    (3.8, 5.0, 2.4, 1.2, '姿态：靠椅', '#B4C8FF', '冷蓝色\n(180,200,255)'),
    (6.9, 5.0, 2.4, 1.2, '姿态：离座', '#888888', '暗灰色\n(80,80,80)'),
    (0.7, 2.4, 2.4, 1.2, '疲劳：OK', '#4CAF50', '8 次绿闪\n0 因子'),
    (3.8, 2.4, 2.4, 1.2, '疲劳：TIRED', '#FFC107', '8 次黄闪\n1 因子'),
    (6.9, 2.4, 2.4, 1.2, '疲劳：REST!', '#F44336', '8 次红闪\n2-3 因子'),
]
for x, y, w, h, t, c, d in led_states:
    style_box(ax, x+w/2, y, w, h, t + '\n' + d, c, fontsize=FS_SMALL, weight='bold')

ax.text(5, 1.0, '疲劳指数 = (HR>85? 1:0) + (SpO2<95? 1:0) + (伏案>45min? 1:0)', ha='center', fontsize=FS_NORMAL, fontweight='bold', color='#333',
    bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825', pad=0.5))

ax.text(5, 0.2, '手势：双击 → 心率测量 | 慢挥手 → 亮度 ±20 | 亮度 0-255', ha='center', fontsize=FS_SMALL, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_led_feedback.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_led_feedback.png saved')

# ============================================================
# FIG 9: 硬件接线图
# ============================================================
fig, ax = plt.subplots(figsize=(16.8, 11.2))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('硬件接线图 · 双MCU + 4传感器 + LED灯条', fontsize=FS_TITLE, fontweight='bold', pad=10)

# AI
ai = mpatches.FancyBboxPatch((0.5, 2.5), 5, 7, boxstyle='round,pad=0.1', facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.8)
ax.add_patch(ai)
ax.text(3, 9.2, 'XIAO ESP32-S3 (AI主板)', ha='center', fontsize=FS_BIG, fontweight='bold', color='#0D47A1')

ai_pins = [
    (1, 7.5, 'D8 (GPIO8)', 'Bus0 SDA'),
    (1, 6.8, 'D9 (GPIO9)', 'Bus0 SCL'),
    (1, 6.1, 'D1 (GPIO1)', 'Bus1 SDA+板间'),
    (1, 5.4, 'D2 (GPIO2)', 'Bus1 SCL+板间'),
    (1, 4.7, 'D6 (GPIO6)', 'WS2812 数据'),
    (1, 4.0, '3.3V', '电源'),
    (1, 3.3, 'GND', '地'),
]
for x, y, pin, func in ai_pins:
    style_box(ax, x+1.0, y, 2.2, 0.45, f'{pin}  {func}', '#BBDEFB', fontsize=FS_SMALL, lw=0.8)

# Display
disp = mpatches.FancyBboxPatch((6.5, 2.5), 5, 7, boxstyle='round,pad=0.1', facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.8)
ax.add_patch(disp)
ax.text(9, 9.2, 'ESP32-C3-DevKitM-1 (显示板)', ha='center', fontsize=FS_BIG, fontweight='bold', color='#1B5E20')

disp_pins = [
    (7, 7.5, 'GPIO4', 'I2C SDA 从机'),
    (7, 6.8, 'GPIO5', 'I2C SCL 从机'),
    (7, 6.1, 'GPIO8', '软I2C OLED+RTC'),
    (7, 5.4, 'GPIO9', '软I2C OLED+RTC'),
    (7, 4.7, 'GPIO21/20', 'USB 串口（未用）'),
    (7, 4.0, '3.3V', '电源'),
    (7, 3.3, 'GND', '地'),
]
for x, y, pin, func in disp_pins:
    style_box(ax, x+1.0, y, 2.2, 0.45, f'{pin}  {func}', '#C8E6C9', fontsize=FS_SMALL, lw=0.8)

# 板间连线
for y1, y2, color, label in [
    (6.1, 6.1, '#D84315', 'D1 <-> GPIO4'),
    (5.4, 5.4, '#EF6C00', 'D2 <-> GPIO5'),
    (4.0, 4.0, '#F44336', '3.3V <-> 3.3V'),
    (3.3, 3.3, '#333333', 'GND <-> GND'),
]:
    ax.plot([3, 7], [y1, y2], '-', color=color, lw=1.5, alpha=0.7)
    ax.text(5, y1+0.2, label, ha='center', fontsize=FS_SMALL, color=color, fontweight='bold')

# 传感器（左侧）
sensors = [
    (0.3, 8.0, 'VL53L0X\n0x29', C_SENSOR),
    (0.3, 6.7, 'TCS34725\n0x29', C_SENSOR),
    (0.3, 5.0, 'MAX30102\n0x57', C_SENSOR),
]
for x, y, t, c in sensors:
    style_box(ax, x+0.55, y, 1.1, 0.8, t, c, fontsize=FS_SMALL, weight='bold')

# 显示（右侧）
displays = [
    (11.0, 8.0, 'SH1106\nOLED', C_HW),
    (11.0, 6.7, 'DS3231\nRTC', C_HW),
]
for x, y, t, c in displays:
    style_box(ax, x-0.55, y, 1.1, 0.8, t, c, fontsize=FS_SMALL, weight='bold')

# LED
ax.add_patch(mpatches.FancyBboxPatch((2.5, 1.2), 2, 0.5, boxstyle='round,pad=0.05', facecolor='#FFECB3', edgecolor='#FF8F00', linewidth=1.2))
ax.text(3.5, 1.45, 'WS2812 LED灯条 × 60', ha='center', fontsize=FS_NORMAL, fontweight='bold')

# Legend
legend = [
    mpatches.Patch(facecolor='#BBDEFB', edgecolor=EDGE_COLOR, label='AI主板引脚'),
    mpatches.Patch(facecolor='#C8E6C9', edgecolor=EDGE_COLOR, label='显示板引脚'),
    mpatches.Patch(facecolor='#D84315', label='板间I2C'),
    mpatches.Patch(facecolor='#333333', label='GND (必须共地)'),
]
ax.legend(handles=legend, loc='lower center', ncol=4, fontsize=FS_LEGEND, bbox_to_anchor=(0.5, -0.04))

plt.tight_layout()
plt.savefig(f'{OUT}/fig_wiring.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_wiring.png saved')

# ============================================================
# FIG 10: 启动诊断序列
# ============================================================
fig, ax = plt.subplots(figsize=(18.2, 4.9))
ax.set_xlim(0, 15)
ax.set_ylim(0, 3)
ax.axis('off')
ax.set_title('AI主板上电启动自检 LED 序列', fontsize=FS_TITLE, fontweight='bold', pad=8)

steps = [
    (0.5, 'Boot', '红', '#F44336', 600),
    (1.9, 'Boot', '绿', '#4CAF50', 600),
    (3.3, 'Boot', '蓝', '#2196F3', 600),
    (4.7, 'Boot', '白', '#FFFFFF', 400),
    (6.2, 'VL53L0X', '紫', '#9C27B0', 300),
    (7.5, 'MAX30102', '青', '#00BCD4', 300),
    (8.8, 'TCS34725', '蓝', '#2196F3', 300),
    (10.2, '结果', '绿/橙/红', '#4CAF50', 2000),
    (12.5, '传感器闪烁', '绿/红', '#FF9800', 1500),
]
for x, phase, color_name, color, duration in steps:
    style_box(ax, x+0.65, 1.9, 1.2, 0.7, phase, color, fontsize=FS_SMALL, weight='bold')
    ax.text(x+0.65, 1.55, f'{duration}ms', ha='center', fontsize=FS_TICK, color='#333')
    ax.text(x+0.65, 1.25, color_name, ha='center', fontsize=FS_TICK, color='#333')
    if x < 12:
        line_arrow(ax, x+1.25, 1.9, x+1.4, 1.9, color='#666', lw=1.0)

ax.text(7.5, 0.5, '总启动 ~6.5s | 全部通过=绿 | 部分故障=橙 | 全部故障=红', ha='center', fontsize=FS_SMALL, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_startup_sequence.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_startup_sequence.png saved')

# ============================================================
# === 新增 3 张图 ===
# ============================================================

# ============================================================
# FIG 11: RTC 软件 I2C 位带时序
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 6.3))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.axis('off')
ax.set_title('RTC 软件 I2C 位带驱动时序 · 写 1 byte', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 时序横轴
ax.plot([1, 11], [0.7, 0.7], 'k-', lw=1.2)
for x in range(1, 12):
    ax.plot([x, x], [0.65, 0.75], 'k-', lw=0.5)
    ax.text(x, 0.4, ['S', 'A6', 'A5', 'A4', 'A3', 'A2', 'A1', 'A0', 'W', 'A', 'D'][x-1], ha='center', fontsize=FS_SMALL, fontweight='bold')

# SDA / SCL 信号
sda_y = 1.6
scl_y = 2.6
ax.text(0.3, sda_y, 'SDA', ha='right', fontsize=FS_SMALL, fontweight='bold', color='#D32F2F')
ax.text(0.3, scl_y, 'SCL', ha='right', fontsize=FS_SMALL, fontweight='bold', color='#1976D2')

# SCL 时钟
for i in range(11):
    x = 1 + i
    ax.plot([x, x+0.7], [scl_y, scl_y], color='#1976D2', lw=1.5)
    ax.plot([x+0.7, x+0.7], [scl_y, scl_y-0.3], color='#1976D2', lw=1.5)
    if i < 10:
        ax.plot([x+0.7, x+1.0], [scl_y-0.3, scl_y-0.3], color='#1976D2', lw=1.5)
        ax.plot([x+1.0, x+1.0], [scl_y-0.3, scl_y], color='#1976D2', lw=1.5)

# SDA 数据（高低）
sda_bits = [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]  # 0x68+W+ACK pattern
for i, bit in enumerate(sda_bits):
    x = 1 + i
    y = sda_y + (0.4 if bit == 1 else -0.4)
    if i > 0:
        prev_x = 1 + (i-1) + 0.7
        prev_bit = sda_bits[i-1]
        prev_y = sda_y + (0.4 if prev_bit == 1 else -0.4)
        ax.plot([prev_x, x], [prev_y, y], color='#D32F2F', lw=1.5)
    ax.plot([x, x+0.7], [y, y], color='#D32F2F', lw=1.5)

# 说明
ax.text(6, 4.0, '起始位 (S) → 7位地址 (0x68) → 写位 (W=0) → 应答 (ACK) → 数据字节 → 应答 → 停止', ha='center', fontsize=FS_SMALL, color='#333',
    bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825', pad=0.4))

ax.text(6, 3.3, '位带驱动：GPIO8/9 软件控制电平，配合 __TIME__/__DATE__ 宏实现编译时 RTC 校准', ha='center', fontsize=FS_SMALL, color='#666', style='italic')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_rtc_timing.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_rtc_timing.png saved')

# ============================================================
# FIG 12: 资源占用对比
# ============================================================
fig, ax = plt.subplots(figsize=(12.6, 7.0))
categories = ['AI主板', '显示板', 'TFLite 模型\n(已开发, 未启用)']
flash = [420, 210, 100]
ram = [85, 45, 50]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, flash, width, label='Flash (KB)', color='#5C9FE6', edgecolor=EDGE_COLOR, linewidth=EDGE_LW)
bars2 = ax.bar(x + width/2, ram, width, label='RAM (KB)', color='#FFB84D', edgecolor=EDGE_COLOR, linewidth=EDGE_LW)

ax.set_ylabel('占用 (KB)', fontsize=FS_NORMAL)
ax.set_title('固件资源占用分析', fontsize=FS_TITLE, fontweight='bold', pad=10)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=FS_SMALL)
ax.legend(fontsize=FS_LEGEND)
ax.grid(axis='y', alpha=0.3)
ax.tick_params(labelsize=FS_TICK)

for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h+5, f'{int(h)}', ha='center', fontsize=FS_SMALL, fontweight='bold')
for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h+5, f'{int(h)}', ha='center', fontsize=FS_SMALL, fontweight='bold')

ax.text(1.5, 350, '注：ESP32-S3 Flash 总 8MB / RAM 512KB；ESP32-C3 Flash 4MB / RAM 400KB', ha='center', fontsize=FS_SMALL, style='italic', color='#666')
ax.text(1.5, 320, 'TFLite 模型可裁剪，当前选用规则算法（详见 §2.7）', ha='center', fontsize=FS_SMALL, style='italic', color='#666')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_resource_usage.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_resource_usage.png saved')

# ============================================================
# FIG 13: 数据流时间线（仿参考图风格）
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 8.4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('系统数据流时间线 · 1Hz 主循环', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 根
style_box(ax, 1.5, 3.5, 2.2, 1.0, 'AI 主板\n1Hz 主循环', C_ROOT, fontsize=FS_BIG, weight='bold')

# 中间
mids = [
    (5, 5.5, '传感器采集\n(50ms)'),
    (5, 3.5, '算法决策\n(20ms)'),
    (5, 1.5, 'LED + I2C 输出\n(30ms)'),
]
for x, y, t in mids:
    style_box(ax, x, y, 2.4, 0.9, t, C_BRANCH, fontsize=FS_NORMAL, weight='bold')

# 右侧
rights = [
    (9.5, 6.2, 'VL53L0X → 15帧\n滑动均值滤波', C_SENSOR),
    (9.5, 4.8, 'TCS34725 → 12帧\n方差分析', C_SENSOR),
    (9.5, 3.5, '姿态 / 手势 /\n疲劳三因子融合', C_FLOW),
    (9.5, 2.0, 'WS2812 灯效\n8次/状态', C_HW),
    (9.5, 0.5, 'I2C 6字节 → C3\nOLED + 番茄钟', C_HW),
]
for x, y, t, c in rights:
    style_box(ax, x, y, 2.4, 0.9, t, c, fontsize=FS_SMALL)

# 流程箭头
curve_arrow(ax, 2.6, 4.0, 3.8, 5.3, color='#1565C0')
curve_arrow(ax, 2.6, 3.5, 3.8, 3.5, color='#666')
curve_arrow(ax, 2.6, 3.0, 3.8, 1.7, color='#2E7D32')

curve_arrow(ax, 6.2, 5.7, 8.3, 6.1, color='#1565C0')
curve_arrow(ax, 6.2, 5.3, 8.3, 4.8, color='#1565C0')
curve_arrow(ax, 6.2, 3.7, 8.3, 3.6, color='#666')
curve_arrow(ax, 6.2, 1.7, 8.3, 2.0, color='#2E7D32')
curve_arrow(ax, 6.2, 1.4, 8.3, 0.5, color='#2E7D32')

ax.text(6, 6.7, '端侧 AI 决策：本地处理，不上云（隐私安全）', ha='center', fontsize=FS_SMALL, color='#D84315', fontweight='bold',
    bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F57F17', pad=0.3))

plt.tight_layout()
plt.savefig(f'{OUT}/fig_dataflow.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_dataflow.png saved')

# ============================================================
# FIG 14: 端云对比 / 隐私架构（仿参考图风格）
# ============================================================
fig, ax = plt.subplots(figsize=(15.4, 8.4))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
ax.set_title('端云架构对比 · 本项目采用端侧 AI', fontsize=FS_TITLE, fontweight='bold', pad=10)

# 左：传统云端
style_box(ax, 2, 5.5, 3.5, 1.0, '传统方案\n云端 AI', C_WARN, fontsize=FS_BIG, weight='bold')
style_box(ax, 2, 4.2, 3.5, 0.7, '传感器 → MCU → WiFi', C_FLOW, fontsize=FS_SMALL)
style_box(ax, 2, 3.2, 3.5, 0.7, '↑ 上传原始数据 ↑', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 2, 2.0, 3.5, 0.7, '云端服务器计算', C_SENSOR, fontsize=FS_SMALL)
style_box(ax, 2, 0.8, 3.5, 0.7, '↓ 下发决策 ↓\n隐私泄露 / 网络依赖', '#FFCDD2', fontsize=FS_SMALL, weight='bold')

# 中间对比
ax.annotate('VS', xy=(6, 3.5), ha='center', va='center', fontsize=22, fontweight='bold', color='#666',
    bbox=dict(boxstyle='circle', facecolor='white', edgecolor='#666', linewidth=1.5))

# 右：本项目端侧
style_box(ax, 10, 5.5, 3.5, 1.0, '本项目\n端侧 AI', C_ROOT, fontsize=FS_BIG, weight='bold')
style_box(ax, 10, 4.2, 3.5, 0.7, '传感器 → ESP32-S3', C_FLOW, fontsize=FS_SMALL)
style_box(ax, 10, 3.2, 3.5, 0.7, '本地决策 (规则+ML)', C_BRANCH, fontsize=FS_SMALL, weight='bold')
style_box(ax, 10, 2.0, 3.5, 0.7, '直接驱动 LED / I2C', C_BRANCH, fontsize=FS_SMALL)
style_box(ax, 10, 0.8, 3.5, 0.7, '全程不上云\n零网络依赖', '#C8E6C9', fontsize=FS_SMALL, weight='bold')

# 顶部比较
ax.text(2, 6.3, '数据流向：用户→云→用户', ha='center', fontsize=FS_SMALL, style='italic', color='#666')
ax.text(10, 6.3, '数据流向：闭环本地', ha='center', fontsize=FS_SMALL, style='italic', color='#2E7D32')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_edge_vs_cloud.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print('fig_edge_vs_cloud.png saved')

print('=' * 50)
print(f'全部 {14} 张图已生成（参照参考图风格：浅色圆角盒 + 细黑边 + 中等字号）')
