# 光合日程AI · 项目规范

每次会话自动遵守以下规则。

## 项目结构

```
C:\zhinenti\                          ← 项目根（CLAUDE.md 在此）
├── CLAUDE.md                          ← 本文件
├── AI_Board\                          ← AI主板固件 (XIAO ESP32-S3)
├── Display_Board\                     ← 显示板固件 (ESP32-C3)
├── ESP32S3_血氧心率.ino               ← 旧版固件
├── competition\                       ← 比赛提交材料
│   ├── technical_report.tex           ← 技术文档（XeLaTeX）
│   ├── gen_all_figs_zh.py             ← matplotlib 图统一生成脚本
│   ├── figs\                          ← 所有图片（13 matplotlib + 12 ref）
│   └── technical_report.pdf           ← 编译产物
├── deepseek_data-2026-05-15\          ← DeepSeek 开发历史
├── gesture_model.h / posture_model.h  ← TFLite 模型
├── .agents\skills\                    ← 项目级 Claude Code skills
├── .claude\settings.local.json        ← 本地配置
└── 光合日程AI——...策划案.pdf          ← 参考 PDF（光电竞赛）
```

## 硬件约定

| 板 | MCU | 关键引脚 |
|---|---|---|
| AI Board | XIAO ESP32-S3 | D8/D9=I²C Bus0 (VL53L0X), D1/D2=I²C Bus1+板间, D6=WS2812 |
| Display | ESP32-C3-DevKitM-1 | GPIO4/5=I²C 从机(0x08), GPIO8/9=软I²C(OLED+RTC) |

传感器：VL53L0X(0x29) / TCS34725(0x29,不同总线) / MAX30102(0x57) / WS2812×60 / SH1106 OLED / DS3231 RTC

## matplotlib 图风格（必须遵守）

```python
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['font.family'] = 'sans-serif'
rcParams['axes.unicode_minus'] = False
```

| 元素 | 字号 |
|---|---|
| 标题 | 15pt |
| 框标题 | 13pt |
| 正文 | 11pt |
| 注释/小字 | 9pt |
| 图例 | 10pt |

| 颜色 | 用途 |
|---|---|
| `#FF8A95` | 根节点（深粉） |
| `#A8E0A0` | 分支节点（浅绿） |
| `#A0D8F0` | 叶子节点（浅蓝） |
| `#FFD8A8` | 硬件节点（浅橙） |
| `#FFB8B8` | 传感器节点 |

**禁用字符**：`²` (SUPERSCRIPT TWO) 和 `↔` (LEFT RIGHT ARROW) — SimHei 缺失。改用 `I2C` 和 `<->`。

**dpi=180**，figsize 控制在 (10-13) × (4-8) 英寸，保持紧凑。

参考样例：`C:\zhinenti\competition\figs\fig_architecture.png`（仿参考 PDF 风格）
参考源：`C:\zhinenti\competition\ref_imgs_view\page06_0[123].png`

## LaTeX 技术文档规范

**编译命令**（双遍交叉引用）：
```bash
cd /c/zhinenti/competition
export PATH="/d/texlive/2026/bin/windows:$PATH"
xelatex -interaction=nonstopmode technical_report.tex
xelatex -interaction=nonstopmode technical_report.tex
```

**必需宏包**：`graphicx` `booktabs` `hyperref` `fancyhdr` `caption` `enumitem` `float` `xcolor` `amssymb`

**四部分结构**（比赛硬性要求）：
1. 场景需求分析报告
2. 技术升级说明报告
3. 实测数据
4. 平台适配性改造说明

**尺寸限制**：PDF ≤ 50MB | 视频 ≤ 100MB (1920×1080)

## 工具链

| 工具 | 路径 | 用途 |
|---|---|---|
| Python | `C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe` | 图表生成、OCR、文件处理 |
| XeLaTeX | `D:\texlive\2026\bin\windows\xelatex.exe` | 中文 PDF 排版 |
| ffmpeg | `C:\ffmpeg\ffmpeg-8.1.1-full_build\bin\` | 视频处理 |
| OBS Studio | `winget install OBSProject.OBSStudio` | 验证视频录制 |
| DashScope API | `DASHSCOPE_API_KEY` 环境变量 | 通义千问 / 通义万相 AI |

## 比赛相关

- 第十四届全国大学生光电设计竞赛（西南区赛）—— 已提交策划案
- 智能装备创新大赛 —— 当前任务
- 团队名：别跟我们作队
- 比赛硬性要求：
  - 技术文档 PDF ≤ 50MB，含 4 部分
  - 验证视频 MP4 ≤ 100MB，1920×1080，无特效

## 学术论文（进行中）

基于本项目撰写可投稿论文，目标：本科/学生学术期刊或会议（中英皆可）。

- 目录：`paper/`（`references.bib` 参考文献、`data/` 原始 CSV、`figs/` 论文图、`analysis/` 画图脚本）
- 三大贡献点：① TCS34725 色彩传感器复用为手势识别（最新颖）② 纯边缘/无摄像头/规则驱动多模态疲劳融合 ③ 系统集成巧思
- **论文 ≠ 比赛材料**：需真实实验数据、诚实定位（proof-of-concept，非医疗诊断），禁止整段复制 `competition/technical_report.tex`
- 相关 skill：`academic-paper`（写作规范）、`collect-experiment-data`（实验协议）
- 实测数据用户可完整采集；串口日志经显示板 USB（AI 板 CDC 已损）

## 常用命令

```bash
# 编译技术文档（双遍）
techpdf

# 重生成全部技术图
genfigs

# 重生成单张图
genfig architecture

# 提取参考图（已有 _view 子目录）
# ls /c/zhinenti/competition/ref_imgs_view/
```
