import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = 'C:/zhinenti/competition/figs'

# ============================================================
# FIG 5: Pomodoro Timer State Machine
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Pomodoro Timer State Machine', fontsize=16, fontweight='bold', pad=15)

# States
states = [
    (1.5, 6.5, 3, 1.5, 'WORK\n40 minutes\n\nLED: Warm White\nOLED: Countdown', '#FFE0B2'),
    (5.5, 6.5, 3, 1.5, 'REST\n5 minutes\n\nLED: Cool Blue\nOLED: Countdown', '#BBDEFB'),
    (3.5, 2.5, 3, 1.5, 'IDLE\n\nLED: Dim Gray\nOLED: Clock Only', '#E0E0E0'),
]

for x, y, w, h, label, color in states:
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.1', facecolor=color, edgecolor='#333', linewidth=2)
    ax.add_patch(box)
    ax.text(x+w/2, y+h/2, label, ha='center', va='center', fontsize=10)

# Transitions
# WORK -> REST (timer expires)
ax.annotate('', xy=(6.5, 7.2), xytext=(4.5, 7.2),
    arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2.5, connectionstyle='arc3,rad=0.3'))
ax.text(5.5, 8.4, 'Work timer expires\n(40 min)', ha='center', fontsize=9, color='#E65100', fontweight='bold')

# REST -> WORK (timer expires)
ax.annotate('', xy=(4.5, 6.5), xytext=(6.5, 6.5),
    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2.5, connectionstyle='arc3,rad=0.3'))
ax.text(5.5, 5.6, 'Rest timer expires\n(5 min)', ha='center', fontsize=9, color='#0D47A1', fontweight='bold')

# IDLE <-> WORK
ax.annotate('', xy=(2.5, 5.8), xytext=(3.5, 4),
    arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2, connectionstyle='arc3,rad=-0.3'))
ax.text(1.8, 4.8, 'I2C cmd=1\n(start)', ha='center', fontsize=8, color='#1B5E20')

ax.annotate('', xy=(4.5, 3.5), xytext=(3, 5.5),
    arrowprops=dict(arrowstyle='->', color='#C62828', lw=2, connectionstyle='arc3,rad=-0.3'))
ax.text(2.2, 4.0, 'I2C cmd=2\n(stop)', ha='center', fontsize=8, color='#B71C1C')

# Legend
ax.text(5, 1.0, 'Triggers: timer expiry (auto) | I2C command from AI Board (manual)',
    ha='center', fontsize=9, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_pomodoro_state.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_pomodoro_state.png saved')

# ============================================================
# FIG 6: Posture Detection Zones
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title('Posture Detection Zones - VL53L0X ToF Distance', fontsize=16, fontweight='bold', pad=15)

# Desk
desk = mpatches.FancyBboxPatch((0.5, 0.5), 11, 1.5, boxstyle='round', facecolor='#F5DEB3', edgecolor='#8D6E63', linewidth=2)
ax.add_patch(desk)
ax.text(6, 1.25, 'DESK SURFACE', ha='center', fontsize=14, fontweight='bold', color='#5D4037')

# Person icon (simplified)
ax.plot([3, 3], [2.5, 5], 'k-', lw=3, alpha=0.7)
ax.plot([3, 2.2], [2.5, 3.2], 'k-', lw=3, alpha=0.7)
ax.plot([3, 3.8], [2.5, 3.2], 'k-', lw=3, alpha=0.7)

# Sensor on desk
sensor = mpatches.FancyBboxPatch((5.5, 1.6), 1.0, 0.5, boxstyle='round', facecolor='#4CAF50', edgecolor='#1B5E20', linewidth=2)
ax.add_patch(sensor)
ax.text(6, 1.85, 'VL53L0X', ha='center', fontsize=7, color='white', fontweight='bold')

# Distance zones
zones = [
    (0.5, 2.0, 3.5, 1.0, 'DESK (0-400mm)\nSitting at desk', '#C8E6C9', '#2E7D32'),
    (4.0, 2.0, 3.5, 1.0, 'LEAN (400-700mm)\nLeaning back', '#FFF9C4', '#F57F17'),
    (7.5, 2.0, 4.0, 1.0, 'AWAY (>700mm)\nUser left desk', '#FFCDD2', '#C62828'),
]
for x, y, w, h, label, color, edge in zones:
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round', facecolor=color, edgecolor=edge, linewidth=1.5, alpha=0.6)
    ax.add_patch(box)
    ax.text(x+w/2, y+h/2, label, ha='center', va='center', fontsize=10, fontweight='bold')

# LED color indicators
leds = [
    (2.25, 3.3, 'LED: Warm White\n(255,220,180)', '#FFE0B2'),
    (5.75, 3.3, 'LED: Cool Blue\n(180,200,255)', '#BBDEFB'),
    (9.5, 3.3, 'LED: Dim Gray\n(80,80,80)', '#E0E0E0'),
]
for x, y, label, color in leds:
    ax.text(x, y, label, ha='center', va='top', fontsize=8, color='#333')
    circle = plt.Circle((x, y-0.15), 0.15, color=color, ec='#333', linewidth=1)
    ax.add_patch(circle)

# Distance scale
for d in range(0, 1100, 100):
    x = 0.5 + d/1000 * 11
    ax.plot([x, x], [4.5, 4.8], 'k-', lw=0.5)
    if d % 200 == 0:
        ax.text(x, 4.9, f'{d}mm', ha='center', fontsize=7)

plt.tight_layout()
plt.savefig(f'{OUT}/fig_posture_zones.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_posture_zones.png saved')

# ============================================================
# FIG 7: I2C Data Protocol Packet Structure
# ============================================================
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title('Inter-MCU I2C Communication Protocol (6-byte Packet @ 1Hz)', fontsize=14, fontweight='bold', pad=15)

# Packet bytes
bytes_data = [
    (0.3, 3.5, 1.2, 1.5, 'Byte 0\n-----', '#E3F2FD'),
    (1.7, 3.5, 1.2, 1.5, 'Byte 1\n-----', '#E3F2FD'),
    (3.1, 3.5, 1.2, 1.5, 'Byte 2\n-----', '#FFF9C4'),
    (4.5, 3.5, 1.2, 1.5, 'Byte 3\n-----', '#FFF9C4'),
    (5.9, 3.5, 1.2, 1.5, 'Byte 4\n-----', '#F3E5F5'),
    (7.3, 3.5, 1.2, 1.5, 'Byte 5\n-----', '#F3E5F5'),
]

labels_top = ['Heart Rate', 'SpO2', 'Fatigue Lvl', 'Posture', 'Gesture', 'Pomodoro']
labels_bot = ['uint8 (0-255)', 'uint8 (0-100%)', '0=OK 1=Tired\n2=Rest!', '0=Desk 1=Lean\n2=Away', 'reserved', '1=Work 2=Idle\n0=no-op']

for i, (x, y, w, h, header, color) in enumerate(bytes_data):
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round', facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+w/2, y+1.1, labels_top[i], ha='center', fontsize=9, fontweight='bold')
    ax.text(x+w/2, y+0.3, labels_bot[i], ha='center', fontsize=8, color='#555')

# Arrow connecting bytes
for i in range(5):
    x = 1.5 + i * 1.4
    ax.annotate('', xy=(x+0.1, 4.25), xytext=(x+0.1, 4.25),
        arrowprops=dict(arrowstyle='->', color='#D84315', lw=1.5))

# Master to Slave indicator
ax.annotate('', xy=(8.5, 5.5), xytext=(1.5, 5.5),
    arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
ax.text(5, 5.7, 'ESP32-S3 (I2C Master) -> ESP32-C3 (I2C Slave @ 0x08)', ha='center', fontsize=10, color='#1565C0', fontweight='bold')

# Timing
ax.text(5, 1.8, 'Transmission rate: 1 Hz | I2C speed: 100 kHz | Timeout: none (fire-and-forget)',
    ha='center', fontsize=9, style='italic', color='#666')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_data_protocol.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_data_protocol.png saved')

# ============================================================
# FIG 8: LED Color Feedback System
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title('LED Color Feedback System', fontsize=16, fontweight='bold', pad=15)

# States with actual LED colors
led_states = [
    (0.5, 5.5, 2.8, 1.8, 'Posture: DESK', '#FFDAB4', 'Warm White\n(255,220,180)\nBrightness: br'),
    (3.6, 5.5, 2.8, 1.8, 'Posture: LEAN', '#B4C8FF', 'Cool Blue\n(180,200,255)\nBrightness: br'),
    (6.7, 5.5, 2.8, 1.8, 'Posture: AWAY', '#666666', 'Dim Gray\n(80,80,80)\nBrightness: br'),
    (0.5, 2.5, 2.8, 1.8, 'Fatigue: OK', '#4CAF50', '8x Green Blink\n3 factors matched: 0'),
    (3.6, 2.5, 2.8, 1.8, 'Fatigue: TIRED', '#FFC107', '8x Yellow Blink\n3 factors matched: 1'),
    (6.7, 2.5, 2.8, 1.8, 'Fatigue: REST!', '#F44336', '8x Red Blink\n3 factors matched: 2-3'),
]

for x, y, w, h, title, color, desc in led_states:
    box = mpatches.FancyBboxPatch((x, y), w, h, boxstyle='round', facecolor=color, edgecolor='#333', linewidth=2)
    ax.add_patch(box)
    ax.text(x+w/2, y+h-0.3, title, ha='center', fontsize=10, fontweight='bold', color='#222')
    ax.text(x+w/2, y+h/2-0.1, desc, ha='center', fontsize=9, color='#333')

# Fatigue scoring formula
ax.text(5, 1.2, 'Fatigue Score = (HR > 85? 1:0) + (SpO2 < 95? 1:0) + (Desk Time > 45min? 1:0)',
    ha='center', fontsize=11, fontweight='bold', color='#333',
    bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825', pad=0.8))

# Gesture control callout
ax.text(5, 0.3, 'Gesture: Double-tap -> HR measurement | Slow wave -> Brightness +/-20 | Brightness range: 0-255',
    ha='center', fontsize=9, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_led_feedback.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_led_feedback.png saved')

# ============================================================
# FIG 9: Hardware Wiring Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Hardware Wiring Diagram', fontsize=16, fontweight='bold', pad=15)

# ESP32-S3
s3_box = mpatches.FancyBboxPatch((0.5, 3), 5, 6.5, boxstyle='round', facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=3)
ax.add_patch(s3_box)
ax.text(3, 9.2, 'XIAO ESP32-S3 (AI Board)', ha='center', fontsize=12, fontweight='bold', color='#0D47A1')

# ESP32-C3
c3_box = mpatches.FancyBboxPatch((6.5, 3), 5, 6.5, boxstyle='round', facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=3)
ax.add_patch(c3_box)
ax.text(9, 9.2, 'ESP32-C3-DevKitM-1 (Display)', ha='center', fontsize=12, fontweight='bold', color='#1B5E20')

# Pin mapping
# AI Board side
ai_pins = [
    (1, 8, 'D8 (GPIO8)', 'I2C Bus 0 SDA'),
    (1, 7.2, 'D9 (GPIO9)', 'I2C Bus 0 SCL'),
    (1, 6.4, 'D1 (GPIO1)', 'I2C Bus 1 SDA + Inter-MCU'),
    (1, 5.6, 'D2 (GPIO2)', 'I2C Bus 1 SCL + Inter-MCU'),
    (1, 4.8, 'D6 (GPIO6)', 'WS2812 LED Data'),
    (1, 4.0, '3.3V', 'Power'),
    (1, 3.3, 'GND', 'Ground'),
]

for x, y, pin, func in ai_pins:
    ax.add_patch(mpatches.FancyBboxPatch((x, y-0.25), 2, 0.5, boxstyle='round', facecolor='#BBDEFB', edgecolor='#1976D2'))
    ax.text(x+0.15, y+0.1, pin, fontsize=7, fontweight='bold')
    ax.text(x+1.1, y+0.1, func, fontsize=7, color='#333')

# Display Board side
disp_pins = [
    (7, 8, 'GPIO4 (SDA)', 'I2C Slave'),
    (7, 7.2, 'GPIO5 (SCL)', 'I2C Slave'),
    (7, 6.4, 'GPIO8 (SDA)', 'SW I2C OLED+RTC'),
    (7, 5.6, 'GPIO9 (SCL)', 'SW I2C OLED+RTC'),
    (7, 4.8, 'GPIO21/20', 'USB Serial (unused)'),
    (7, 4.0, '3.3V', 'Power'),
    (7, 3.3, 'GND', 'Ground'),
]

for x, y, pin, func in disp_pins:
    ax.add_patch(mpatches.FancyBboxPatch((x, y-0.25), 2, 0.5, boxstyle='round', facecolor='#C8E6C9', edgecolor='#388E3C'))
    ax.text(x+0.15, y+0.1, pin, fontsize=7, fontweight='bold')
    ax.text(x+1.1, y+0.1, func, fontsize=7, color='#333')

# Inter-MCU connections (colored lines)
connections = [
    (3, 6.4, 7, 6.4, '#D84315', 'D1(GPIO1) -> GPIO4'),
    (3, 5.6, 7, 5.6, '#EF6C00', 'D2(GPIO2) -> GPIO5'),
    (3, 4.0, 7, 4.0, '#F44336', '3.3V -> 3.3V'),
    (3, 3.5, 7, 3.5, '#333333', 'GND -> GND'),
]
for x1, y1, x2, y2, color, label in connections:
    ax.plot([x1, x2], [y1+0.1, y2+0.1], '-', color=color, lw=2, alpha=0.7)
    ax.text(5, y1+0.3, label, ha='center', fontsize=7, color=color, fontweight='bold')

# Sensor components (left side)
sensors = [
    (0.3, 8.5, 'VL53L0X\n(0x29)', '#FFCDD2'),
    (0.3, 7.0, 'TCS34725\n(0x29)', '#C8E6C9'),
    (0.3, 5.0, 'MAX30102\n(0x57)', '#BBDEFB'),
]
for x, y, label, color in sensors:
    ax.add_patch(mpatches.FancyBboxPatch((x, y-0.2), 1.1, 0.8, boxstyle='round', facecolor=color, edgecolor='#333'))
    ax.text(x+0.55, y+0.2, label, ha='center', fontsize=7)

# Display components (right side)
displays = [
    (9.7, 8.5, 'SH1106\nOLED', '#FFF9C4'),
    (9.7, 7.0, 'DS3231\nRTC', '#E1BEE7'),
]
for x, y, label, color in displays:
    ax.add_patch(mpatches.FancyBboxPatch((x, y-0.2), 1.1, 0.8, boxstyle='round', facecolor=color, edgecolor='#333'))
    ax.text(x+0.55, y+0.2, label, ha='center', fontsize=7)

# WS2812 LED strip
ax.add_patch(mpatches.FancyBboxPatch((2.5, 1.5), 2, 0.6, boxstyle='round', facecolor='#FFECB3', edgecolor='#FF8F00', linewidth=2))
ax.text(3.5, 1.8, 'WS2812 LED Strip x60', ha='center', fontsize=8, fontweight='bold')

# Legend
legend = [
    mpatches.Patch(color='#BBDEFB', label='AI Board Pin'),
    mpatches.Patch(color='#C8E6C9', label='Display Board Pin'),
    mpatches.Patch(color='#D84315', label='Inter-MCU I2C'),
    mpatches.Patch(color='#333333', label='GND (must share!)'),
]
ax.legend(handles=legend, loc='lower center', ncol=4, fontsize=8)

plt.tight_layout()
plt.savefig(f'{OUT}/fig_wiring.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_wiring.png saved')

# ============================================================
# FIG 10: Startup Diagnostic Sequence
# ============================================================
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 3)
ax.axis('off')
ax.set_title('AI Board Startup Diagnostic LED Sequence', fontsize=14, fontweight='bold', pad=10)

steps = [
    (0.5, 'Boot', 'Red', '#F44336', 600),
    (2, 'Boot', 'Green', '#4CAF50', 600),
    (3.5, 'Boot', 'Blue', '#2196F3', 600),
    (5, 'Boot', 'White', '#FFFFFF', 400),
    (6.5, 'VL53L0X', 'Purple', '#9C27B0', 300),
    (8, 'MAX30102', 'Cyan', '#00BCD4', 300),
    (9.5, 'TCS34725', 'Blue', '#2196F3', 300),
    (11, 'Result', 'Green/Orange/Red', '#4CAF50', 2000),
    (13.5, 'Sensor Blink', 'G/R per sensor', '#FF9800', 1500),
]

for x, phase, color_name, color, duration in steps:
    box = mpatches.FancyBboxPatch((x, 1.5), 1.3, 0.8, boxstyle='round', facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+0.65, 2.1, phase, ha='center', fontsize=8, fontweight='bold')
    ax.text(x+0.65, 1.7, f'{duration}ms', ha='center', fontsize=7)
    ax.text(x+0.65, 1.35, color_name, ha='center', fontsize=7, color='#333')
    # Arrow to next
    if x < 13:
        ax.annotate('', xy=(x+1.3, 2.0), xytext=(x+1.35, 2.0),
            arrowprops=dict(arrowstyle='->', color='#666'))

ax.text(8, 0.7, 'Total startup time: ~6.5s | All 3 sensors OK = Green, Partial = Orange, None = Red',
    ha='center', fontsize=9, style='italic', color='#555')

plt.tight_layout()
plt.savefig(f'{OUT}/fig_startup_sequence.png', dpi=200, bbox_inches='tight', facecolor='white')
print('fig_startup_sequence.png saved')

print('All 6 new diagrams generated!')
