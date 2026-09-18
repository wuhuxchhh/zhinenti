---
name: academic-paper
description: 为「光合日程AI」项目撰写可投稿的本科/学生级学术论文（中/英）。含 IMRaD 结构、贡献点定位、诚实写作、引用规范、审稿人自查清单。
---

# 学术论文写作规范

为「光合日程AI」多模态桌面健康感知系统撰写可投稿论文。目标 venue：本科/学生学术期刊或会议（中英皆可）。

**核心原则：论文 ≠ 比赛材料。** 比赛材料允许 datasheet 推算和营销话术；论文必须有真实实验数据、诚实定位、可复现。**严禁把 `competition/technical_report.tex` 的段落直接搬进论文**（自我抄袭 + 语气不符），只可复用图表和事实。

## 三个可主打的贡献点（按含金量）

1. **颜色传感器 TCS34725 的手势识别复用**——最新颖。市面手势方案用 APDS-9960/摄像头/雷达；用 2 元色彩传感器做时序方差手势是罕见点。论文里作为 primary contribution。
2. **纯边缘、无摄像头、规则驱动的多模态疲劳融合**——差异化：非可穿戴、桌面、隐私友好、超低成本；且"弃 TFLite 选规则"要给出量化论证（精度/延迟/flash/功耗）。
3. **系统集成 + 工程巧思**——双 I2C 解 0x29 冲突、软件 I2C 位带 RTC、6 字节板间协议、闭环氛围光反馈。作为 secondary contributions 或"system design"章节。

## IMRaD 结构（会议 6-8 页 / 期刊 8-12 页）

1. **Abstract**（150-250 词）：问题→方法→关键结果数字→意义。必须含真实实验数字。
2. **Introduction**：久坐健康危害动机 → 现有方案不足（摄像头隐私/可穿戴负担/云延迟成本）→ 本文贡献（bullet 列 2-3 条）。
3. **Related Work**：按 related-work 调研的 A-G 主题组织，每主题末尾点明"本文差异"。
4. **System Design / Methods**：
   - 硬件架构（双 MCU 框图，复用 `competition/figs/fig_architecture.png`）
   - 颜色传感器手势算法（时序方差 + 双击，复用 `fig_gesture_flowchart.png`，给公式）
   - ToF 姿态分类、疲劳融合规则（给判据 HR>85/SpO2<95/久坐>45min）
   - 双 I2C 拓扑、板间协议、氛围光反馈
5. **Experiments / Results**：见 `collect-experiment-data` skill 产出的真实数据——手势混淆矩阵、姿态准确率、HR/SpO2 vs 参考仪 Bland-Altman、功耗、延迟、板间丢包、RTC 漂移、规则 vs TFLite 对比表。
6. **Discussion**：结果解读 + **诚实的局限性**（下节）。
7. **Conclusion & Future Work**。
8. **References**。

## 必须诚实写出的局限性（审稿人一定问，主动写反而加分）

- 心率/血氧需主动按手指触发（双击），非连续被动监测。
- 疲劳阈值是启发式，未经临床验证——定位 proof-of-concept，勿称"诊断"。
- "姿态"实为人脸到传感器距离（前倾代理量），非脊柱角度。
- 色彩传感器手势受环境光影响——用实验说明鲁棒性边界。
- 被试样本量小、非临床人群。

## 引用与 LaTeX

- 参考文献存 `paper/references.bib`（仅收录已核实的条目）。
- 默认模板 **IEEEtran**（会议）——学生会议最通用；投中文刊再换。
- 编译：`xelatex → bibtex → xelatex → xelatex`（中文用 ctexart + IEEEtran 或直接中文刊模板）。
- 引用风格跟 venue：IEEE 数字制 `[1]`。

## 图表复用

`competition/figs/` 已有 25 张图。论文可直接复用架构图、手势流程图、疲劳曲线、I2C 拓扑、板间协议、资源占用。**新增图必须来自真实实验数据**（混淆矩阵、Bland-Altman、功耗曲线）——由 `collect-experiment-data` 生成，别再用推算值。matplotlib 风格沿用 CLAUDE.md 约定，但论文图用英文标注（若投英文刊）。

## 投稿前自查清单

- [ ] 摘要含真实实验数字（非推算）
- [ ] 贡献点 2-3 条明确列出
- [ ] Related work 每主题点明本文差异
- [ ] 所有引用真实可核实（无编造 DOI）
- [ ] 局限性章节诚实完整
- [ ] 未从比赛文档整段复制（自查重）
- [ ] 图表为真实数据、分辨率 ≥300dpi
- [ ] 定位为 proof-of-concept，无过度医疗声称
- [ ] 作者/单位/团队"别跟我们作队"署名确认
