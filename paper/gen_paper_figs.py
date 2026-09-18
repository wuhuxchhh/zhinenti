# -*- coding: utf-8 -*-
"""论文实验结果图（预期值，最终稿以实测替换）。风格遵循 CLAUDE.md。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['font.family'] = 'sans-serif'
rcParams['axes.unicode_minus'] = False

DPI = 300
OUT = "figs/"

C_ROOT = '#FF8A95'; C_BRANCH = '#A8E0A0'; C_LEAF = '#A0D8F0'
C_HW = '#FFD8A8'; C_WARN = '#FFB8B8'

FS_TITLE = 15; FS_LABEL = 12; FS_TICK = 11; FS_ANNO = 10


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print("saved", name)


# ---------- E1 手势混淆矩阵 ----------
def gesture_confusion():
    labels = ['双击', '慢挥增亮', '慢挥减亮', '静止']
    cm = np.array([
        [57, 1, 0, 2],
        [1, 55, 3, 1],
        [0, 3, 54, 3],
        [1, 1, 0, 58],
    ])
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    im = ax.imshow(cm, cmap='Greens')
    ax.set_xticks(range(4)); ax.set_yticks(range(4))
    ax.set_xticklabels(labels, fontsize=FS_TICK)
    ax.set_yticklabels(labels, fontsize=FS_TICK)
    ax.set_xlabel('预测类别', fontsize=FS_LABEL)
    ax.set_ylabel('真实类别', fontsize=FS_LABEL)
    ax.set_title('手势识别混淆矩阵（每类 60 次）', fontsize=FS_TITLE)
    thr = cm.max() / 2
    for i in range(4):
        for j in range(4):
            ax.text(j, i, cm[i, j], ha='center', va='center',
                    color='white' if cm[i, j] > thr else 'black', fontsize=FS_LABEL)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    save(fig, 'fig_gesture_confusion.png')


# ---------- E1 不同光照准确率 ----------
def gesture_lighting():
    conds = ['暗光', '室内常光', '明亮', '窗边强光']
    acc = [94.2, 95.4, 90.1, 86.3]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    bars = ax.bar(conds, acc, color=[C_BRANCH, C_LEAF, C_HW, C_WARN], edgecolor='k', linewidth=1)
    ax.set_ylim(80, 100)
    ax.set_ylabel('识别准确率 (%)', fontsize=FS_LABEL)
    ax.set_title('不同环境光下的手势识别准确率', fontsize=FS_TITLE)
    ax.tick_params(labelsize=FS_TICK)
    for b, a in zip(bars, acc):
        ax.text(b.get_x() + b.get_width() / 2, a + 0.3, f'{a:.1f}', ha='center', fontsize=FS_ANNO)
    ax.grid(axis='y', ls='--', alpha=0.4)
    save(fig, 'fig_gesture_lighting.png')


# ---------- E2 坐姿评测 ----------
def posture_eval():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    rng = np.random.default_rng(7)
    # 散点：真实距离 vs 测量距离
    zones = {'伏案': (250, 400, C_WARN), '正常': (450, 700, C_HW), '离席': (750, 1000, C_LEAF)}
    ax = axes[0]
    for name, (lo, hi, c) in zones.items():
        true = rng.uniform(lo, hi, 30)
        meas = true + rng.normal(0, true * 0.03)
        ax.scatter(true, meas, s=28, color=c, edgecolor='k', linewidth=0.4, label=name, alpha=0.85)
    lim = [200, 1050]
    ax.plot(lim, lim, 'k--', lw=1, alpha=0.6)
    for b in (400, 700):
        ax.axvline(b, color='gray', ls=':', lw=1)
        ax.axhline(b, color='gray', ls=':', lw=1)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel('真实距离 (mm)', fontsize=FS_LABEL)
    ax.set_ylabel('测量距离 (mm)', fontsize=FS_LABEL)
    ax.set_title('(a) 距离测量一致性', fontsize=FS_TITLE)
    ax.legend(fontsize=FS_ANNO); ax.tick_params(labelsize=FS_TICK)
    # 混淆矩阵
    labels = ['伏案', '正常', '离席']
    cm = np.array([[29, 1, 0], [2, 27, 1], [0, 0, 30]])
    ax = axes[1]
    im = ax.imshow(cm, cmap='Blues')
    ax.set_xticks(range(3)); ax.set_yticks(range(3))
    ax.set_xticklabels(labels, fontsize=FS_TICK); ax.set_yticklabels(labels, fontsize=FS_TICK)
    ax.set_xlabel('预测区', fontsize=FS_LABEL); ax.set_ylabel('真实区', fontsize=FS_LABEL)
    ax.set_title('(b) 三区分类混淆矩阵', fontsize=FS_TITLE)
    thr = cm.max() / 2
    for i in range(3):
        for j in range(3):
            ax.text(j, i, cm[i, j], ha='center', va='center',
                    color='white' if cm[i, j] > thr else 'black', fontsize=FS_LABEL)
    save(fig, 'fig_posture_eval.png')


# ---------- E3 Bland-Altman ----------
def bland_altman():
    rng = np.random.default_rng(3)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    # HR
    ref = rng.uniform(62, 92, 40)
    dev = ref + rng.normal(-1.2, 3.0, 40)
    _ba(axes[0], ref, dev, '心率 (bpm)', C_LEAF)
    axes[0].set_title('(a) 心率 Bland-Altman', fontsize=FS_TITLE)
    # SpO2
    ref2 = rng.uniform(95, 99, 40)
    dev2 = ref2 + rng.normal(0.4, 1.4, 40)
    _ba(axes[1], ref2, dev2, 'SpO2 (%)', C_BRANCH)
    axes[1].set_title('(b) 血氧 Bland-Altman', fontsize=FS_TITLE)
    save(fig, 'fig_bland_altman.png')


def _ba(ax, ref, dev, unit, color):
    mean = (ref + dev) / 2
    diff = dev - ref
    md = diff.mean(); sd = diff.std(ddof=1)
    ax.scatter(mean, diff, s=26, color=color, edgecolor='k', linewidth=0.4, alpha=0.85)
    ax.axhline(md, color='r', lw=1.2, label=f'均值差 {md:.1f}')
    ax.axhline(md + 1.96 * sd, color='gray', ls='--', lw=1, label=f'+1.96SD {md+1.96*sd:.1f}')
    ax.axhline(md - 1.96 * sd, color='gray', ls='--', lw=1, label=f'-1.96SD {md-1.96*sd:.1f}')
    ax.set_xlabel(f'均值 {unit}', fontsize=FS_LABEL)
    ax.set_ylabel(f'差值 (设备-参考) {unit}', fontsize=FS_LABEL)
    ax.legend(fontsize=9); ax.tick_params(labelsize=FS_TICK)
    ax.grid(ls='--', alpha=0.35)


# ---------- E4 疲劳 vs KSS ----------
def fatigue_kss():
    t = np.array([0, 15, 30, 45, 60])
    sys = np.array([0, 0, 1, 1, 2])
    kss = np.array([3, 4, 5, 6, 7])
    fig, ax1 = plt.subplots(figsize=(7, 4.3))
    l1 = ax1.step(t, sys, where='post', color=C_ROOT, lw=2.2, marker='o', label='系统疲劳等级')
    ax1.set_xlabel('伏案时间 (min)', fontsize=FS_LABEL)
    ax1.set_ylabel('系统疲劳等级 (0/1/2)', fontsize=FS_LABEL, color=C_ROOT)
    ax1.set_yticks([0, 1, 2]); ax1.set_yticklabels(['OK', 'Tired', 'Rest'])
    ax1.tick_params(axis='y', labelcolor=C_ROOT, labelsize=FS_TICK)
    ax1.tick_params(axis='x', labelsize=FS_TICK)
    ax2 = ax1.twinx()
    l2 = ax2.plot(t, kss, color='#3070C0', lw=2.2, marker='s', ls='--', label='KSS 自评')
    ax2.set_ylabel('KSS 嗜睡量表 (1-9)', fontsize=FS_LABEL, color='#3070C0')
    ax2.set_ylim(1, 9); ax2.tick_params(axis='y', labelcolor='#3070C0', labelsize=FS_TICK)
    ax1.set_title('系统疲劳等级与 KSS 自评随时间变化', fontsize=FS_TITLE)
    lines = l1 + l2
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper left', fontsize=FS_ANNO)
    save(fig, 'fig_fatigue_kss.png')


# ---------- E5 规则 vs TFLite ----------
def rule_vs_ml():
    metrics = ['Flash (KB)', 'RAM (KB)', '决策时延 (ms)']
    rule = [2, 0.8, 0.1]
    ml = [82, 18, 6]
    x = np.arange(len(metrics)); w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    b1 = ax.bar(x - w / 2, rule, w, label='规则融合', color=C_BRANCH, edgecolor='k', linewidth=1)
    b2 = ax.bar(x + w / 2, ml, w, label='TFLite Micro', color=C_HW, edgecolor='k', linewidth=1)
    ax.set_yscale('log')
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=FS_TICK)
    ax.set_ylabel('数值（对数轴）', fontsize=FS_LABEL)
    ax.set_title('规则融合与 TFLite Micro 资源/时延对照', fontsize=FS_TITLE)
    ax.legend(fontsize=FS_ANNO)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.1,
                    f'{b.get_height():g}', ha='center', fontsize=FS_ANNO)
    ax.grid(axis='y', ls='--', alpha=0.4)
    save(fig, 'fig_rule_vs_ml.png')


if __name__ == '__main__':
    gesture_confusion()
    gesture_lighting()
    posture_eval()
    bland_altman()
    fatigue_kss()
    rule_vs_ml()
    print('done')
