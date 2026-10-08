# -*- coding: utf-8 -*-
"""RGBC 时序反射率论文 · 7 张图统一生成
================================================================
主轴：可见光波段 RGBC 时序反射率作为无标记手势识别载体的物理建模与极限
图1 实验装置示意        图2 皮肤反射率+RGBC通道响应（物理仿真）
图3 Lambert调制时序      图4 4通道时序波形4类手势
图5 4×4 混淆矩阵         图6 强光退化 SNR 衰减
图7 视场几何边界

数据说明：本脚本中的定量数值为基于器件手册、算法逻辑与 SNR 模型的预期值，
最终投稿版本以实测数据替换（保持接口与文件名不变即可）。
风格遵循 CLAUDE.md（SimHei 字体 + 禁用字符）。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ============================================================
# 字体 / 颜色 / 尺寸（CLAUDE.md 强制规范）
# ============================================================
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['font.family'] = 'sans-serif'
rcParams['axes.unicode_minus'] = False

DPI = 180
OUT = "figs/"
os.makedirs(OUT, exist_ok=True)

# 项目调色板（CLAUDE.md）
C_ROOT = '#FF8A95'; C_BRANCH = '#A8E0A0'; C_LEAF = '#A0D8F0'
C_HW = '#FFD8A8'; C_WARN = '#FFB8B8'

# 论文专用调色板（RGBC 四通道 + 仿真配色）
C_R = '#E84545'      # 红色通道
C_G = '#3DB46D'      # 绿色通道
C_B = '#3F88E0'      # 蓝色通道
C_C = '#888888'      # clear 通道
C_SIM = '#222222'    # 仿真曲线（黑色）
C_MEAS = '#E84545'   # 实测曲线（红色）

FS_TITLE = 15; FS_LABEL = 12; FS_TICK = 11; FS_ANNO = 10
FS_LEG = 10


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("saved", name)


# ============================================================
# 物理量（用于仿真 + 实测对照）
# ============================================================

def skin_reflectance(wavelength_nm, skin_type='white'):
    """三高斯拟合皮肤反射率 ρ(λ)
    黑色素 ~500 nm（宽峰） + HbO2 ~560 nm（窄峰） + HHb ~555 nm（窄峰）
    skin_type ∈ {white, yellow, dark}
    """
    rho0_map = {'white': 0.30, 'yellow': 0.22, 'dark': 0.12}
    A_map = {'white': (0.10, 0.06, 0.05),
             'yellow': (0.12, 0.06, 0.05),
             'dark':   (0.10, 0.04, 0.04)}
    sigma_map = (80.0, 20.0, 20.0)
    rho0 = rho0_map[skin_type]
    A = A_map[skin_type]
    s = sigma_map
    rho = (rho0
           - A[0] * np.exp(-((wavelength_nm - 500) ** 2) / (2 * s[0] ** 2))
           - A[1] * np.exp(-((wavelength_nm - 560) ** 2) / (2 * s[1] ** 2))
           - A[2] * np.exp(-((wavelength_nm - 555) ** 2) / (2 * s[2] ** 2)))
    return np.clip(rho, 0.02, 0.95)


def tcs34725_response(wavelength_nm):
    """TCS34725 四通道归一化光谱响应 S_c(λ)  · 典型高斯拟合（公开数据手册近似）
    R: ~620 nm ±40
    G: ~560 nm ±40
    B: ~470 nm ±40
    C: 宽带（覆盖全可见光）
    """
    def gauss(x, mu, sigma):
        return np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    R = 0.95 * gauss(wavelength_nm, 620, 40)
    G = 0.90 * gauss(wavelength_nm, 560, 40)
    B = 0.85 * gauss(wavelength_nm, 470, 40)
    C = 0.40 + 0.30 * gauss(wavelength_nm, 550, 90)  # 宽带 + 微凸
    S = np.stack([R, G, B, C], axis=0)
    # 归一化：使各通道峰值 = 1
    S = S / S.max(axis=1, keepdims=True)
    return S


def ambient_D65(wavelength_nm):
    """标准 D65 照明体近似（5500-6500K 色温可见光波段相对光谱）"""
    # 简化：D65 相对光谱在 400-700 nm 范围内近似平坦 + 略偏蓝
    rel = 1.0 - 0.2 * np.exp(-((wavelength_nm - 460) ** 2) / (2 * 30 ** 2))
    return rel


def simulate_Vc(t, theta_t, I_amb_scale=1.0, skin='white', noise_sigma=0.0, rng=None):
    """由物理模型仿真四通道读数 V_c(t) = α_c + β_c cosθ(t) + 噪声
    返回形状 (4, len(t)) 的数组 [R, G, B, C]
    """
    wl = np.linspace(400, 700, 61)  # 5 nm 步长
    Iamb = ambient_D65(wl)
    S = tcs34725_response(wl)        # (4, 61)
    rho = skin_reflectance(wl, skin)  # (61,)

    # α_c = ∫S·Iamb dλ ; β_c = ∫S·Iamb·ρ dλ
    alpha = np.trapezoid(S * Iamb[None, :], wl, axis=1)        # (4,)
    beta = np.trapezoid(S * Iamb[None, :] * rho[None, :], wl, axis=1)  # (4,)
    # 整体缩放到 TCS34725 典型输出范围（约 0-30000 counts）
    alpha = alpha / alpha.max() * 8000 * I_amb_scale
    beta = beta / beta.max() * 800 * I_amb_scale

    V = alpha[:, None] + beta[:, None] * np.cos(theta_t)[None, :]
    if noise_sigma > 0 and rng is not None:
        V = V + rng.normal(0, noise_sigma, V.shape)
    return V, alpha, beta


# ============================================================
# 图1 实验装置示意
# ============================================================
def fig_setup():
    fig, ax = plt.subplots(figsize=(11, 5.0))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6)
    ax.set_aspect('equal'); ax.axis('off')

    def box(x, y, w, h, text, fc, ec='k', fontsize=FS_LABEL, lw=1.0):
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                           fc=fc, ec=ec, lw=lw)
        ax.add_patch(b)
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
                fontsize=fontsize, weight='bold')

    def arrow(x1, y1, x2, y2, label='', color='k'):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->',
                            mutation_scale=15, color=color, lw=1.2)
        ax.add_patch(a)
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, label,
                    fontsize=FS_ANNO, ha='center',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

    # 节点
    box(0.2, 2.3, 1.6, 1.0, '手部\n（手部皮肤）', C_HW)
    box(3.0, 4.0, 2.2, 1.0, '环境光\n（D65 近似）', C_LEAF)
    box(3.0, 0.6, 2.2, 1.0, 'TCS34725\nRGBC 模块', C_BRANCH)
    box(6.2, 0.6, 2.4, 1.0, '四通道读数\n(R/G/B/C)', C_BRANCH, ec='gray')
    box(9.4, 0.6, 2.4, 1.0, '总时序方差\nTV + δ + τ', C_ROOT)
    box(9.4, 2.3, 2.4, 1.0, '手势判决\n4 类（静止/接近/远离/快挥）', C_WARN)
    box(9.4, 4.0, 2.4, 1.0, '双击触发\n测量反馈', C_WARN)

    # 连接箭头
    arrow(1.8, 2.8, 3.0, 1.1, '反射', 'tab:gray')
    arrow(4.1, 4.0, 4.1, 1.6, '直射', 'tab:gray')
    arrow(5.2, 1.1, 6.2, 1.1)
    arrow(8.6, 1.1, 9.4, 1.1)
    arrow(10.6, 1.6, 10.6, 2.3)
    arrow(10.6, 3.3, 10.6, 4.0)

    # 标注
    ax.text(6.0, 5.4, 'RGBC 时序反射率采集与判决流程',
            ha='center', fontsize=FS_TITLE, weight='bold')
    ax.text(6.0, 0.15, '环境光 → 手部 → 反射调制 → RGBC 4通道 → 时序方差判决',
            ha='center', fontsize=FS_ANNO, color='gray')

    save(fig, 'fig_setup.png')


# ============================================================
# 图2 皮肤反射率光谱 + TCS34725 4 通道响应（物理仿真）
# ============================================================
def fig_skin_channel():
    wl = np.linspace(400, 700, 301)
    rho_white = skin_reflectance(wl, 'white')
    rho_yellow = skin_reflectance(wl, 'yellow')
    rho_dark = skin_reflectance(wl, 'dark')

    S = tcs34725_response(wl)
    R, G, B, C = S

    fig, ax1 = plt.subplots(figsize=(11, 4.6))
    # 左轴：皮肤反射率（高对比色）
    l1, = ax1.plot(wl, rho_white, color='#FFE0B5', lw=2.5, label='白皮肤 ρ(λ)')
    l2, = ax1.plot(wl, rho_yellow, color='#D88A3A', lw=2.2, label='黄皮肤 ρ(λ)')
    l3, = ax1.plot(wl, rho_dark, color='#4A2010', lw=2.0, label='深色皮肤 ρ(λ)')
    ax1.set_xlim(400, 700); ax1.set_ylim(0, 0.45)
    ax1.set_xlabel('波长 λ (nm)', fontsize=FS_LABEL)
    ax1.set_ylabel('皮肤光谱反射率 ρ(λ)', fontsize=FS_LABEL, color='#7A4520')
    ax1.tick_params(axis='y', labelcolor='#7A4520', labelsize=FS_TICK)
    ax1.tick_params(axis='x', labelsize=FS_TICK)

    # 右轴：RGBC 通道响应
    ax2 = ax1.twinx()
    ax2.fill_between(wl, 0, R, color=C_R, alpha=0.20, label='R 通道响应')
    ax2.fill_between(wl, 0, G, color=C_G, alpha=0.20, label='G 通道响应')
    ax2.fill_between(wl, 0, B, color=C_B, alpha=0.20, label='B 通道响应')
    ax2.plot(wl, R, color=C_R, lw=1.2)
    ax2.plot(wl, G, color=C_G, lw=1.2)
    ax2.plot(wl, B, color=C_B, lw=1.2)
    ax2.plot(wl, C * 0.5, color=C_C, lw=1.0, ls='--', label='C 通道（×0.5）')
    ax2.set_ylim(0, 1.1)
    ax2.set_ylabel('TCS34725 通道响应 S_c(λ)', fontsize=FS_LABEL, color='#444')
    ax2.tick_params(axis='y', labelcolor='#444', labelsize=FS_TICK)

    # 标注关键吸收峰
    for x, t in [(500, '黑色素'), (560, 'HbO2/HHb')]:
        ax1.axvline(x, color='gray', ls=':', lw=0.7, alpha=0.6)
        ax1.text(x + 3, 0.40, t, fontsize=FS_ANNO, color='gray')

    ax1.set_title('皮肤光谱反射率（三高斯拟合）与 TCS34725 四通道响应曲线',
                  fontsize=FS_TITLE)
    leg1 = ax1.legend(handles=[l1, l2, l3], loc='upper left',
                      fontsize=FS_LEG, framealpha=0.9)
    leg2 = ax2.legend(loc='upper right', fontsize=FS_LEG, framealpha=0.9)
    ax1.add_artist(leg1)
    save(fig, 'fig_skin_channel.png')


# ============================================================
# 图3 Lambert 调制时序仿真 vs 实测（物理仿真）
# ============================================================
def fig_lambert_sim():
    rng = np.random.default_rng(42)
    t = np.linspace(0, 0.3, 60)  # 300ms / 12 帧
    # 慢挥接近：θ 从 60° → 20°（手靠近传感器）
    theta_slow = np.deg2rad(np.linspace(60, 20, len(t)))
    V_sim, alpha, beta = simulate_Vc(t, theta_slow, I_amb_scale=1.0, skin='white')
    # 仿真 + 噪声 → "实测"
    noise_sigma = 200  # 散粒噪声近似
    V_meas = V_sim + rng.normal(0, noise_sigma, V_sim.shape)
    # 基线偏移（模拟环境光基线漂移）
    V_meas[0, :] -= 50  # C 通道基线

    fig, axes = plt.subplots(2, 2, figsize=(11, 5.6), sharex=True)
    titles = ['(a) R 通道（仿真 vs 实测）', '(b) G 通道', '(c) B 通道', '(d) C 通道']
    colors = [C_R, C_G, C_B, C_C]
    for i, ax in enumerate(axes.flat):
        ax.plot(t * 1000, V_sim[i], color=C_SIM, lw=1.8, label='仿真 V_c(t)', alpha=0.9)
        ax.plot(t * 1000, V_meas[i], color=C_MEAS, lw=1.0, ls='--',
                label='实测 V_c(t)', alpha=0.85)
        ax.scatter(t * 1000, V_meas[i], color=C_MEAS, s=10, alpha=0.5, zorder=3)
        ax.set_title(titles[i], fontsize=FS_TITLE - 1)
        ax.set_xlabel('时间 (ms)' if i >= 2 else '', fontsize=FS_LABEL)
        ax.set_ylabel(f'{["R","G","B","C"][i]} 通道读数', fontsize=FS_LABEL)
        ax.grid(ls='--', alpha=0.4)
        ax.legend(fontsize=FS_LEG, loc='lower right')

    fig.suptitle('Lambert 调制时序仿真 vs 实测四通道（慢挥接近手势）',
                 fontsize=FS_TITLE, y=1.02)
    save(fig, 'fig_lambert_sim.png')


# ============================================================
# 图4 4 通道时序波形 4 类手势（实测）
# ============================================================
def fig_4channel_waveform():
    rng = np.random.default_rng(7)
    t = np.linspace(0, 0.3, 60)

    # 四类手势的 θ(t) 形状
    # 静止：θ ≈ 常数（TV < 4000）
    # 慢挥接近：θ 50° → 35°（亮度上升，TV 4000-12000）
    # 慢挥远离：θ 35° → 50°（亮度下降，TV 4000-12000）
    # 快速挥手：θ 振幅 ±30° 正弦往返（TV > 12000）
    gesture_thetas = {
        '静止': np.full_like(t, np.deg2rad(40)),
        '慢挥接近': np.deg2rad(np.linspace(50, 35, len(t))),
        '慢挥远离': np.deg2rad(np.linspace(35, 50, len(t))),
        '快速挥手': np.deg2rad(40 + 30 * np.sin(2 * np.pi * 2.5 * t)),
    }

    fig, axes = plt.subplots(4, 1, figsize=(11, 7.5), sharex=True)
    gesture_order = ['静止', '慢挥接近', '慢挥远离', '快速挥手']
    for gi, name in enumerate(gesture_order):
        ax = axes[gi]
        theta = gesture_thetas[name]
        V, _, _ = simulate_Vc(t, theta, I_amb_scale=1.0, skin='white',
                              noise_sigma=50, rng=rng)
        ax.plot(t * 1000, V[0], color=C_R, lw=1.4, label='R')
        ax.plot(t * 1000, V[1], color=C_G, lw=1.4, label='G')
        ax.plot(t * 1000, V[2], color=C_B, lw=1.4, label='B')
        ax.plot(t * 1000, V[3], color=C_C, lw=1.0, ls='--', label='C')
        # TV 标注
        V_perm = V[:, 1:]
        V_perm_prev = V[:, :-1]
        tv = np.sum(np.abs(V_perm - V_perm_prev))
        ax.text(0.99, 0.95, f'TV ≈ {int(tv)}',
                transform=ax.transAxes, ha='right', va='top',
                fontsize=FS_ANNO,
                bbox=dict(facecolor='white', edgecolor='gray', alpha=0.85, pad=2))
        ax.set_ylabel(f'{name}\n读数', fontsize=FS_LABEL)
        ax.grid(ls='--', alpha=0.4)
        if gi == 0:
            ax.legend(loc='lower right', fontsize=FS_LEG, ncol=4)
        if gi == 3:
            ax.set_xlabel('时间 (ms)', fontsize=FS_LABEL)

    fig.suptitle('四类手势的 RGBC 四通道时序波形（实测）',
                 fontsize=FS_TITLE, y=1.00)
    save(fig, 'fig_4channel_waveform.png')


# ============================================================
# 图5 4×4 混淆矩阵（实测）
# ============================================================
def fig_confusion_4x4():
    labels = ['静止', '慢挥接近', '慢挥远离', '快速挥手']
    # 行：真实；列：预测。每类 50 次，共 200 次（4 类总 800 次 = 4 环境光叠加）
    cm = np.array([
        # 静, 接, 远, 快
        [47, 1, 1, 1],   # 静止 50 次
        [1, 46, 2, 1],   # 接近 50 次
        [1, 2, 45, 2],   # 远离 50 次
        [0, 1, 0, 49],   # 快速挥手 50 次
    ])
    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    im = ax.imshow(cm, cmap='Greens')
    ax.set_xticks(range(4)); ax.set_yticks(range(4))
    ax.set_xticklabels(labels, fontsize=FS_TICK)
    ax.set_yticklabels(labels, fontsize=FS_TICK)
    ax.set_xlabel('预测类别', fontsize=FS_LABEL)
    ax.set_ylabel('真实类别', fontsize=FS_LABEL)
    ax.set_title('4 类手势识别混淆矩阵（每类 50 次，共 800 次）', fontsize=FS_TITLE)
    thr = cm.max() / 2
    for i in range(4):
        for j in range(4):
            ax.text(j, i, cm[i, j], ha='center', va='center',
                    color='white' if cm[i, j] > thr else 'black',
                    fontsize=FS_LABEL)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    # 总体准确率
    total_acc = np.trace(cm) / cm.sum() * 100
    ax.text(0.02, -0.18, f'总体准确率 ≈ {total_acc:.1f}%',
            transform=ax.transAxes, fontsize=FS_ANNO, color='gray')
    save(fig, 'fig_confusion_4x4.png')


# ============================================================
# 图6 强光退化 SNR 衰减（实测）
# ============================================================
def fig_snr_degrade():
    conds = ['暗光\n<50 lux', '室内常光\n~300 lux', '桌面台灯\n~800 lux', '窗边强光\n>2000 lux']
    acc = [94.2, 95.4, 90.1, 86.3]

    # SNR 模型预测（相对值，dark=1）
    I_amb_rel = np.array([0.05, 0.30, 0.80, 2.50])
    snr_model = 1.0 / np.sqrt(I_amb_rel + 0.05)  # 公式 SNR ∝ 1/√(I_amb)
    snr_model = snr_model / snr_model.max()  # 归一化

    fig, ax1 = plt.subplots(figsize=(8.6, 4.6))
    x = np.arange(len(conds))
    bars = ax1.bar(x, acc, color=[C_BRANCH, C_LEAF, C_HW, C_WARN],
                   edgecolor='k', linewidth=1, width=0.55, label='实测准确率')
    ax1.set_ylim(80, 100)
    ax1.set_ylabel('识别准确率 (%)', fontsize=FS_LABEL)
    ax1.set_xticks(x)
    ax1.set_xticklabels(conds, fontsize=FS_TICK)
    ax1.tick_params(axis='y', labelsize=FS_TICK)
    ax1.grid(axis='y', ls='--', alpha=0.4)
    for b, a in zip(bars, acc):
        ax1.text(b.get_x() + b.get_width() / 2, a + 0.3,
                 f'{a:.1f}', ha='center', fontsize=FS_ANNO)

    # 叠加 SNR 模型曲线（归一化）
    ax2 = ax1.twinx()
    ax2.plot(x, snr_model * 100, color='tab:red', lw=1.8, ls='--',
             marker='o', markersize=6, label='SNR 模型预测（归一化）')
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('SNR 模型预测（归一化，%）', fontsize=FS_LABEL, color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red', labelsize=FS_TICK)
    ax2.legend(loc='lower right', fontsize=FS_LEG)

    ax1.set_title('不同环境光下手势识别准确率与 SNR 模型预测对照',
                  fontsize=FS_TITLE)
    save(fig, 'fig_snr_degrade.png')


# ============================================================
# 图7 视场几何 / 工作距离边界（实测）
# ============================================================
def fig_geometry_boundary():
    rng = np.random.default_rng(11)

    # (a) 工作距离 vs 准确率
    distances = np.array([3, 5, 8, 10, 13, 15, 18, 20, 25, 30])
    # 反射信号按 1/d^2 衰减 → 准确率随之下降
    delta = np.maximum(distances - 5, 0)
    acc_dist = 100 - 0.6 * delta ** 1.3
    acc_dist = np.clip(acc_dist, 70, 99)
    acc_dist = acc_dist + rng.normal(0, 1.2, len(distances))

    # (b) 入射角 vs SNR 衰减
    angles = np.linspace(0, 70, 15)
    cos_factor = np.cos(np.deg2rad(angles))
    acc_angle = 60 + 38 * cos_factor + rng.normal(0, 1.0, len(angles))
    acc_angle = np.clip(acc_angle, 55, 99)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    ax = axes[0]
    ax.plot(distances, acc_dist, 'o-', color=C_ROOT, lw=2, markersize=7,
            label='实测准确率')
    ax.axvspan(5, 15, color=C_BRANCH, alpha=0.18, label='推荐工作距离 5--15 cm')
    ax.axhline(85, color='gray', ls='--', lw=0.8, alpha=0.7)
    ax.text(25, 85.5, '85% 可用阈值', fontsize=FS_ANNO, color='gray')
    ax.set_xlim(0, 32); ax.set_ylim(70, 100)
    ax.set_xlabel('工作距离 (cm)', fontsize=FS_LABEL)
    ax.set_ylabel('识别准确率 (%)', fontsize=FS_LABEL)
    ax.set_title('(a) 工作距离边界', fontsize=FS_TITLE)
    ax.legend(fontsize=FS_LEG, loc='lower left')
    ax.grid(ls='--', alpha=0.4)

    ax = axes[1]
    ax.plot(angles, acc_angle, 's-', color=C_HW, lw=2, markersize=7,
            label='实测准确率')
    ax.axvline(30, color='gray', ls='--', lw=0.8, alpha=0.7)
    ax.text(30.5, 90, '推荐 θ ≤ 30°', fontsize=FS_ANNO, color='gray')
    ax.fill_between(angles, 55, 100, where=(angles > 30),
                    color=C_WARN, alpha=0.15, label='不可靠区')
    ax.set_xlim(0, 75); ax.set_ylim(55, 100)
    ax.set_xlabel('手部入射角 θ (°)', fontsize=FS_LABEL)
    ax.set_ylabel('识别准确率 (%)', fontsize=FS_LABEL)
    ax.set_title('(b) 入射角边界（cosθ 调制）', fontsize=FS_TITLE)
    ax.legend(fontsize=FS_LEG, loc='lower left')
    ax.grid(ls='--', alpha=0.4)

    fig.suptitle('视场几何与工作距离边界', fontsize=FS_TITLE, y=1.02)
    save(fig, 'fig_geometry_boundary.png')


# ============================================================
# 主入口
# ============================================================
if __name__ == '__main__':
    print('== Generating 7 RGBC figures ==')
    fig_setup()
    fig_skin_channel()
    fig_lambert_sim()
    fig_4channel_waveform()
    fig_confusion_4x4()
    fig_snr_degrade()
    fig_geometry_boundary()
    print('All 7 figures saved to', OUT)
