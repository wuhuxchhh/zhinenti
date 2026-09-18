# Claude Code 工作痕迹恢复（2026-06-20 → 2026-09-18）

**生成时间**：2026-09-18（今天会话内）
**结论**：Claude Code 上本项目的**完整对话 jsonl 已全部被 9/15 自动清理删掉**，无法恢复。本文档是从残存的"工作证据"中反向汇总出来的"影子历史"，帮助后续会话快速了解项目曾做过什么。

---

## 1. 时间线（基于可验证证据）

| 日期 | 事件 | 证据来源 |
|---|---|---|
| 2026-04-09 ~ 2026-05-15 | 项目用 **DeepSeek** 开发（不是 Claude Code） | `deepseek_data-2026-05-15/conversations.json` 索引第 103 条"AI光合日程加入血氧心率"（505 条消息） |
| 2026-05-14 | 在 DeepSeek 上调研"ChatGPT API 连接 Claude 方案"、"微信远程遥控 Claude Code 方案"——为迁移做准备 | deepseek #99、#100 |
| **2026-06-20** | **首次 git 提交** "光合日程AI 双MCU项目"；同日创建 `.agents/skills/dashscope-image-gen/` ——**项目正式迁入 Claude Code** | git log bada433；文件系统 mtime |
| 2026-06-27 | 创建 `.agents/skills/compile-pdf/`、`gen-tech-figs/`、`rec-verify-video/` ——**比赛材料工具集** | 文件系统 mtime |
| 2026-07-15 | 创建 `.agents/skills/academic-paper/`、`collect-experiment-data/` ——**期刊论文 + 实验数据协议** | 文件系统 mtime |
| 2026-07-15 17:03 | 项目根目录里有 `光合日程AI——基于番茄学习的多模态智能番茄钟.pdf`（3.1MB，光电设计竞赛策划书/技术文档） | 文件系统 mtime（来自回收站恢复的 18MB jsonl 中的一条工具调用输出） |
| 2026-09-15 04:22:15 | **Claude Code 自动清理触发**，删除 `~/.claude/projects/C--zhinenti/` 下所有旧会话 jsonl | `~/.claude/.last-cleanup` 时间戳 |
| **2026-09-18** | 当前会话开始。Claude Code 上本项目唯一残留的会话 | `c8b99bd0-3766-448e-9e10-2e4cfe5bc4b6.jsonl` |

---

## 2. Claude Code 上做过的几大类工作（从 settings.local.json 的 47 条 allow 反推）

### 2.1 比赛技术文档（光电竞赛）
- `Bash(xelatex -interaction=nonstopmode technical_report.tex)`
- `Bash(techpdf)`、`genfigs`、`genfig`、`showfig`、`techdoc`、`recvideo`、`znstatus`
- 触发 `Skill(gen-tech-figs)`、`Skill(compile-pdf)`、`Skill(rec-verify-video)`
- 14 张图由 `competition/gen_all_figs_zh.py` 生成，统一 SimHei、dpi=180、浅色圆角盒风格
- 验证视频 ≤100MB MP4、1920×1080、无特效（用 OBS 录）
- **成果**：`competition/technical_report.pdf` + `competition/figs/`（13 matplotlib + 12 ref）

### 2.2 期刊论文（投期刊用）
- `Bash(xelatex -interaction=nonstopmode paper.tex)` + 双遍交叉引用
- `Bash(bibtex paper *)`
- `Bash(mv fig_posture_zones.png fig_design_posture.png)` 等 4 次图重命名
- `Read(//c/c/zhinenti/paper/**)` —— 注：路径 `c/c/zhinenti` 可能是 typo（重复 c）
- `WebFetch(domain:pubmed.ncbi.nlm.nih.gov)` —— 查文献
- `Bash(grep -c "^\\\\bibitem" paper.bbl)` —— 统计参考文献数量
- **成果**：`paper/paper.tex` + `paper/paper.pdf` + `paper/references.bib` + `paper/figs/`（6 张）

### 2.3 Skills 体系搭建
7 个 skills 在 `.agents/skills/`：
- `academic-paper` —— 期刊论文写作规范（IMRaD、贡献点定位、引用规范）
- `collect-experiment-data` —— 真实实验数据采集协议（HR/SpO2/手势/姿态/功耗）
- `compile-pdf` —— XeLaTeX 双遍编译
- `dashscope-image-gen` —— 通义万相 AI 画图
- `gen-tech-figs` —— matplotlib 14 张技术图统一生成
- `rec-verify-video` —— 比赛验证视频录制（OBS）

### 2.4 硬件 / 固件（基于 deepseek 历史 + 项目源码推断）
- 双 MCU：AI 主板 XIAO ESP32-S3 + 显示板 ESP32-C3-DevKitM-1
- 传感器：VL53L0X (姿态) / TCS34725 (手势复用) / MAX30102 (HR/SpO2)
- 板间通信：I²C 6 字节包，主→从 0x08
- 已知硬件坑：AI 板 USB CDC 损坏只能 ROM 烧录；VL53L0X 无 XSHUT 必须独占总线
- **注意**：完整的固件调试对话已丢失，只能从 git 源码 + memory 中恢复

---

## 3. 已经永久丢失的内容

以下内容**已无法恢复**，只能从 git 源码 / 现有 skills / paper 草稿中重新理解：

| 类别 | 损失程度 | 影响 |
|---|---|---|
| 代码调试对话（"为什么这个传感器读数不对"等） | 全部丢失 | 需要重新调代码时只能从源码反推 |
| 当时的设计取舍讨论（"为什么选规则而不是 TFLite"等） | 全部丢失 | academic-paper skill 里保留了结论，但理由讨论没了 |
| 实验数据采集的完整过程 | 全部丢失 | collect-experiment-data skill 保留了协议，但实际跑了多少、效果如何未知 |
| 板间通信协议演进过程 | 全部丢失 | 当前 6 字节格式是最终态，中间方案讨论没了 |
| 失败尝试记录 | 全部丢失 | 哪些方案试过失败、为什么放弃都不知道 |

---

## 4. 后续防御措施（防止再丢）

1. **关键决策及时 commit + 写 ADR**：在 `paper/decisions/` 或类似位置记录"为什么选 X 方案"
2. **定期把 `~/.claude/projects/C--zhinenti/*.jsonl` 备份到项目目录**（建议放进 `paper/session_backups/`，写个脚本每周跑）
3. **长会话结束时用 `/exit`**，不要被强杀；被强杀的会话可能没有 `.jsonl` 落盘
4. **写 paper 前先读**：
   - `paper/deepseek_recovered/103_main_project.md`（4-9 ~ 5-15 决策链）
   - 本文件（6-20 ~ 9-18 工作痕迹）

---

## 5. 当前 Claude Code 工具链提示

- 用 `techpdf`、`genfigs`、`genfig <name>` 等 shell 函数（来自 `znenv.sh`）
- 编译命令：`xelatex -interaction=nonstopmode technical_report.tex` 双遍
- Python：`C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe`
- XeLaTeX：`D:\texlive\2026\bin\windows\xelatex.exe`
- ffmpeg：`C:\ffmpeg\ffmpeg-8.1.1-full_build\bin\`
- DASHSCOPE_API_KEY 已配置在 `.claude/settings.local.json` env