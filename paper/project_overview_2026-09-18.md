# 光合日程AI · 项目总览（2026-09-18 抢救快照）

> **目的**：Claude Code 历史会话被 9/15 自动清理全部删除。本文从源码、git、skills、PDF、paper 草稿、deepseek 历史中反向汇总，作为后续所有会话的"项目大脑"。
>
> **生成时间**：2026-09-18
> **下次更新触发**：硬件改板 / 算法重写 / 比赛材料大改 / 论文投稿前

---

## 1. 项目一句话

**桌面端无摄像头多模态疲劳感知系统**——用 XIAO ESP32-S3（AI 主板）+ ESP32-C3（显示板）双 MCU，融合 ToF 坐姿 / TCS34725 色彩手势 / MAX30102 血氧心率 / 番茄钟状态，通过 WS2812 灯环反馈，**纯边缘、纯规则、零摄像头**。

**作者**：whuxchhh | **团队**：别跟我们作队 | **比赛**：第十四届全国大学生光电设计竞赛（西南区赛）+ 智能装备创新大赛 + 期刊投稿（进行中）

---

## 2. 双 MCU 硬件架构（最终态）

### 2.1 AI 主板（XIAO ESP32-S3，21×17.5mm）

| 功能 | GPIO | 说明 |
|---|---|---|
| I²C Bus0 | D8(SDA)/D9(SCL) | **VL53L0X** ToF 测距（0x29） |
| I²C Bus1 | D1(SDA)/D2(SCL) | **TCS34725**（0x29）+ **MAX30102**（0x57）+ 板间通信（0x08 从机地址发往显示板） |
| WS2812 | D6 | 60 颗灯环，状态反馈（呼吸/警告/呼吸法） |
| USB CDC | — | **已损坏，只能 ROM 烧录**（重大坑） |

### 2.2 显示板（ESP32-C3-DevKitM-1）

| 功能 | GPIO | 说明 |
|---|---|---|
| I²C 板间（硬件） | GPIO4(SDA)/GPIO5(SCL) | 主机 @ 0x08，从 AI 板 6 字节包 1Hz |
| 软 I²C（OLED + RTC） | GPIO9(SCL)/GPIO8(SDA) | **SH1106 OLED 128×64** + **DS3231 RTC**（软件 bit-bang 同一总线） |
| USB CDC | — | **可用**——所有调试串口日志从显示板 USB 出 |

### 2.3 关键坑（必须记住）

1. **VL53L0X 没有 XSHUT 引脚**，地址硬编码 0x29 → 必须独占 I²C 总线（这就是为什么用双总线）
2. **TCS34725 也是 0x29** → 放 Bus1，且启动时要先确认 VL53L0X 已就绪
3. **AI 板 USB CDC 损坏** → 烧录走 ROM 模式（按住 BOOT + RST），所有日志从显示板看
4. **DS3231 + OLED 同一软 I²C 总线** → 必须 bit-bang，软件协议驱动（详见 Display_Board.ino）

---

## 3. 三大光学通道与物理原理（论文核心卖点）

### 3.1 940nm ToF 通道（VL53L0X）

- **物理原理**：SPAD（单光子雪崩二极管）阵列 + 飞行时间测量
- **输出**：距离（mm）
- **算法**：15 样本滑动均值 → 三档分箱
  - `<400mm` = 伏案（chin on chest）
  - `400–700mm` = 靠椅（upright）
  - `>700mm` = 离座（away）
- **论文价值**：低功耗、隐私友好、纯边缘

### 3.2 660/940nm PPG 通道（MAX30102）

- **物理原理**：Beer-Lambert 定律，光强变化 → 血容量脉动 → 心率；红光/红外比例 → 血氧饱和度
- **输出**：HR (bpm) + SpO₂ (%)
- **算法**：库自带 `MAX30102.getHeartRate()` / `getSpO2()`
- **诚实定位**：**不是医疗级**，proof-of-concept，仅趋势监测

### 3.3 VIS RGBC 通道（TCS34725，**最创新**）

- **物理原理**：4 通道（R/G/B/Clear）硅光电二极管，积分时间可调
- **复用为手势**：12 帧 RGBC 时序方差
  - `TV < 4000` = 静态（无手势）
  - `TV > 12000` = 快速挥手（返回 -2）
  - `TV ∈ [4000, 12000]` 且 R/G/B 比例变化 = 慢速接近（+2）或远离（+3）
  - **双击检测**：800ms 内两次接近事件
- **论文最大贡献**：单传感器多任务——同 TCS34725 既测环境色温又能识别手势
- **未做的事**：色温自适应白光补偿（论文 future work）

---

## 4. 算法栈（纯规则，无 ML）

### 4.1 疲劳融合（核心）

```c
// 三个二值因子加权
fat = (vh && hr > 85 ? 1 : 0)         // 心率偏高
    + (vs && sp < 95 ? 1 : 0)          // 血氧偏低
    + (posture == 0 && pmin >= 45 ? 1 : 0);  // 伏案≥45 分钟

// 0 = OK（绿灯呼吸）
// 1 = Tired（黄灯慢闪）
// 2 = Rest!（红灯快闪 + 蜂鸣器 + 强制休息）
```

### 4.2 番茄钟

```c
WORK_SEC = 40UL * 60;  // 40 分钟
REST_SEC = 5UL * 60;   // 5 分钟
```

### 4.3 板间 6 字节协议（1Hz）

```
字节 0: HR (uint8)
字节 1: SpO₂ (uint8)
字节 2: 疲劳等级 0/1/2
字节 3: 姿态 0/1/2
字节 4: 手势 -2/-1/2/3
字节 5: 命令（显示板 → AI 板：进入休息/退出休息）
```

---

## 5. TFLite 模型状态（开发了但没用）

| 模型 | 文件 | 用途 | 状态 |
|---|---|---|---|
| `gesture_model.h` | 71KB | 手势识别 TFLite Micro | **训练完成，未部署** |
| `posture_model.h` | 123KB | 坐姿分类 TFLite Micro | **训练完成，未部署** |

**为什么不用**：规则算法在当前精度/算力/功耗权衡下已经够用，且 TFLite Micro 推理耗电约 80mA vs 规则版 15mA。论文里写"edge rule-based"是卖点之一。

**未来**：如果想升级，posture_model.h 可以替换 15 样本均值分箱为 5 类精细姿态。

---

## 6. 两条并行轨道

### 6.1 比赛轨道（competition/）—— 已基本完成

| 文件 | 状态 |
|---|---|
| `competition/technical_report.tex` (689 行) | ✅ 已编译通过 |
| `competition/technical_report.pdf` | ✅ 已生成 |
| `competition/gen_all_figs_zh.py` (717 行) | ✅ 14 张图统一生成 |
| `competition/figs/` | ✅ 13 matplotlib + 12 ref |
| 验证视频 | ⏳ 待录（≤100MB, 1920×1080, 无特效, 用 OBS） |

**比赛硬性要求**：
- PDF ≤ 50MB
- 视频 ≤ 100MB
- 四部分结构：①场景需求分析 ②技术升级说明 ③实测数据 ④平台适配性改造

### 6.2 期刊轨道（paper/）—— 进行中

| 文件 | 状态 |
|---|---|
| `paper/paper.tex` (330 行) | ✅ IMRaD 框架，7 图 |
| `paper/paper.pdf` | ✅ 已编译 |
| `paper/references.bib` (329 行) | ✅ 30+ 引用，覆盖 8 个主题 |
| `paper/figs/` 6 张结果图 | ⚠️ **seed-based 合成数据占位** |
| `paper/user_figs/README.md` 16 张锁定图 | ✅ 用户 PDF 导出锁定 |
| 实测数据采集 | ⏳ **最关键待办** |

**论文三大贡献点**（不可让步）：
1. **TCS34725 色彩传感器复用为手势**（最新颖）
2. **纯边缘 / 无摄像头 / 规则驱动多模态疲劳融合**
3. **系统集成巧思**（双 MCU + 双 I²C 总线解决地址冲突 + 软 I²C 共享）

**诚实定位**：proof-of-concept，非医疗诊断，禁止整段复制 `competition/technical_report.tex`。

---

## 7. Skills 体系（.agents/skills/，7 个）

| Skill | 创建时间 | 用途 |
|---|---|---|
| `dashscope-image-gen` | 2026-06-20 | 通义万相 AI 画图 |
| `compile-pdf` | 2026-06-27 | XeLaTeX 双遍编译 |
| `gen-tech-figs` | 2026-06-27 | matplotlib 14 张技术图统一生成 |
| `rec-verify-video` | 2026-06-27 | 比赛验证视频录制（OBS） |
| `academic-paper` | 2026-07-15 | 期刊论文写作规范（IMRaD、贡献点、引用） |
| `collect-experiment-data` | 2026-07-15 | 真实实验数据采集协议（HR/SpO2/手势/姿态/功耗） |

**调谁用 Skill 工具**，shell 函数（techpdf/genfigs/genfig/showfig/techdoc/recvideo/znstatus）来自 `znenv.sh`。

---

## 8. 工具链速查

| 工具 | 路径 |
|---|---|
| Python | `C:/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe` |
| XeLaTeX | `D:\texlive\2026\bin\windows\xelatex.exe` |
| ffmpeg | `C:\ffmpeg\ffmpeg-8.1.1-full_build\bin\` |
| DashScope API | `DASHSCOPE_API_KEY` 已配 `~/.claude/settings.local.json` |

**PostToolUse hook**：编辑 `.tex` 文件时自动 xelatex 重编译。

---

## 9. 关键设计决策（不要再讨论）

| 决策 | 理由 | 出处 |
|---|---|---|
| 双 MCU 而非单 MCU 双核 | 隔离实时感知 vs UI 显示任务，避免 OLED 刷新卡顿 | deepseek #103 |
| 双 I²C 总线（Bus0 + Bus1） | VL53L0X 与 TCS34725 都是 0x29，无 XSHUT 必须分总线 | hardware-setup.md |
| 规则算法而非 TFLite | 当前精度足够，功耗省 65mA | academic-paper skill |
| 番茄 40/5 而非经典 25/5 | 大学长时间伏案场景 | deepseek #103 |
| 6 字节板间协议 | 刚好覆盖所有状态字段 + 1Hz 足够 | Display_Board.ino |
| OLED + RTC 软 I²C 共享 | ESP32-C3 硬件 I²C 留给板间通信 | Display_Board.ino |

---

## 10. 当前待办（按优先级）

### P0（论文投稿前必须完成）

- [ ] **真实实验数据采集**（`collect-experiment-data` skill 有协议）
  - HR/SpO2：坐姿不动测 5 分钟，看稳定性
  - 手势：4 类 × 50 次 = 200 样本，混淆矩阵
  - 姿态：3 类 × 30 次 = 90 样本，停留 30s/次
  - 疲劳：自评 KSS 量表 + 系统评分对照，≥ 20 人次
  - 功耗：电流表测 AI 板 vs 显示板，规则 vs TFLite 对比
- [ ] 替换 `paper/gen_paper_figs.py` 中的 seed-based 占位为实测数据
- [ ] Bland-Altman 图：MAX30102 vs 指夹血氧仪（如果有的话）

### P1（比赛收尾）

- [ ] OBS 录验证视频（≤100MB, 1920×1080）
- [ ] 检查 PDF 大小 ≤ 50MB

### P2（未来改进）

- [ ] TFLite 部署功耗对比实测
- [ ] TCS34725 色温自适应白光补偿
- [ ] 加 BLE 把数据传到手机

---

## 11. 不要犯的错（feedback 记忆）

1. **不要整段复制 competition/technical_report.tex 到 paper/paper.tex**——比赛风格 vs 期刊风格完全不同
2. **不要"无摄像头"被理解成"低隐私"**——论文里要强调 edge + no-network + no-camera 三件套
3. **不要把 SpO₂ 当医疗数据**——必须 disclaimer："仅供学习参考，非医疗器械"
4. **不要假设用户记得之前怎么做的**——Claude Code 历史已丢，重读 `paper/deepseek_recovered/103_main_project.md` 和本文
5. **不要让会话裸跑**——长任务结束时建议用户手动 `/exit` 而不是强杀（强杀可能没落盘）

---

## 12. 文件索引（快速跳）

| 想找什么 | 看哪 |
|---|---|
| 硬件接线 | `~/.claude/projects/C--zhinenti/memory/hardware-setup.md` |
| AI 板固件 | `C:\zhinenti\AI_Board\AI_Board.ino` |
| 显示板固件 | `C:\zhinenti\Display_Board\Display_Board.ino` |
| 比赛技术文档 | `C:\zhinenti\competition\technical_report.tex` |
| 期刊论文 | `C:\zhinenti\paper\paper.tex` |
| 参考文献 | `C:\zhinenti\paper\references.bib` |
| 项目决策链 | `C:\zhinenti\paper\deepseek_recovered\103_main_project.md` |
| Claude Code 工作痕迹 | `C:\zhinenti\paper\claude_code_history_recovered.md` |
| 实验协议 | `C:\zhinenti\.agents\skills\collect-experiment-data\SKILL.md` |
| 论文写作规范 | `C:\zhinenti\.agents\skills\academic-paper\SKILL.md` |

---

**维护说明**：每次重大改动后（硬件改板 / 算法重写 / 比赛材料大改 / 论文投稿前），更新本文对应章节。

---

## 13. PDF 全文回顾（2026-09-18 抢救完成）

四份 PDF 全部读取完毕。要点合并如下（与本文件第 2-6 节有冗余时优先信任本文）。

### 13.1 策划案 PDF（2.4MB，19 页，2026-04 撰写，b02z8lxT）

**原始设计**（最终未全采用）：
- **单 MCU**：XIAO ESP32C3 + 微信小程序（**未实现**——最终改为 XIAO ESP32-S3 + ESP32-C3 双 MCU）
- **4 个 TFLite Micro 模型**（总 <15KB）：坐姿 / 手势 / 疲劳 / 学习专注度（**只实现了 2 个**，且最终未部署）
- **姿态颜色**：伏案 255,220,180（暖橙）/ 靠椅 180,200,255（冷蓝）/ 离座 80,80,80（暗灰）
- **成本**：原型 200-255 元 → 量产 180 元 → 终端 199-299 元
- **市场调研**：87% 需要智能桌面助手，76% 关注隐私

### 13.2 paper.pdf = paper光.pdf（19 页，2026-08-01，期刊投稿版）

> 两份文件**正文完全一致**，仅 paper光.pdf 每页加了"光合日程 AI"页眉。最终以 paper.pdf 为准即可。

**题目**：面向资源受限双 MCU 平台的无摄像头桌面健康感知系统：基于 RGBC 颜色传感器复用的手势交互与可解释疲劳提醒

**作者团队**：别跟我们作队

**四大贡献**：
1. **物理方法**：RGBC 颜色传感器复用为短时序反射变化探测器（**最新颖**）
2. **物理建模**：显式给出三条通道的物理模型与极限
3. **系统集成**：双 MCU 资源受限平台协同 + 传感器级数据最小化
4. **实验物理**：三通道实测验证 + Bland-Altman 一致性分析

**三条通道物理模型**（论文核心公式）：
| 通道 | 物理原理 | 关键公式 |
|---|---|---|
| 940nm ToF | SPAD 单光子探测 + 光子渡越时间 | `d = c·∆t / 2`，SPAD 抖动 ~百 ps → mm 级距离分辨率 |
| 660/940nm PPG | Beer-Lambert 定律 | `I = I₀·e^(-ε(λ)·c·l)`，AC/DC 比 → SpO₂ |
| VIS RGBC | 光谱反射率时序变化 | `TV = Σ_{i=1}^{L-1}(|R_i-R_{i-1}|+|G_i-G_{i-1}|+|B_i-B_{i-1}|+|C_i-C_{i-1}|)` |

**物理常数**：
- WS2812 峰值波长：625nm（红）/ 525nm（绿）/ 470nm（蓝）
- 皮肤 VIS 反射率 ~0.15-0.30，红高蓝低，与黑色素相关
- VL53L0X VCSEL 脉冲宽度 ~10ns，量程 30-1200mm
- PPG：双击触发，采集 100 样本（红光 + 红外）
- RGBC：积分时间 24ms，增益 16×，12 帧窗口

**RGBC 手势算法阈值**：T_static = 4000，T_fast = 12000，δ = 800，τ = 800ms（双击间隔）

**疲劳融合规则**（论文式 3）：
```
s = 𝟙[HR>85] + 𝟙[SpO₂<95] + 𝟙[伏案且久坐≥45min]
s=0 → OK 绿 / s=1 → Tired 黄 / s≥2 → Rest 红
```

**板间协议**：6 字节定长，1Hz，I²C 从机 0x08
```
[HR uint8] [SpO₂ uint8] [疲劳 0/1/2] [姿态 0/1/2] [手势 预留] [Cmd]
```

**实验结果**（注：脚注明示"**本节定量指标为依据器件数据手册与算法逻辑得到的预期值，最终投稿版本将以实测数据替换**"）：
- 15 名被试（20-26 岁，男女各半）× 4 种环境光（暗光/室内常光/明亮/窗边强光）
- 手势识别 ~93%，双击 ~95%，误触 ~4%，窗边强光下降 ~8pp
- 坐姿三区分类 ~96%，距离测量相对误差 ±3%
- 心率 MAE ~3 bpm，血氧 MAE ~2%
- 疲劳 vs KSS 自评 Spearman ρ ≈ 0.6

**规则 vs TFLite Micro 实测对照（表 1，图 15）**：
| 指标 | 规则融合 | TFLite Micro |
|---|---|---|
| 准确率 / F1 | ≈0.92 | ≈0.93 |
| Flash | ≈2 KB | ≈82 KB |
| RAM（含 arena） | <1 KB | ≈18 KB |
| 单次决策时延 | <0.1 ms | ≈6 ms |
| 可解释性 | 高 | 低 |

**系统级指标**：
- 板间通信 1h 丢包 <0.5%
- RTC 24h 漂移 ±2s（约 23ppm）
- 端到端时延 ~120ms

**5 个相关工作领域**：
1. 手势识别（非接触交互）：视觉 / 超声 / 毫米波 / APDS-9960
2. 边缘多模态疲劳检测：驾驶场景为主
3. 无接触姿态/在座：ToF / 毫米波 / WiFi CSI / 压力椅
4. 规则 vs TinyML：CMSIS-NN / TFLite Micro / MLPerf Tiny
5. 办公健康干预：升降桌 / 提醒 / ambient display

**6 条明确 Limitations**（论文第 5 节）：
1. HR/SpO₂ 为双击按需间歇测量，依赖指尖接触稳定性，Beer-Lambert 标定在散射组织下偏离
2. 疲劳阈值（85/95/45min）为工程启发式，未经临床验证
3. "坐姿"实为单点 1D-ToF 几何代理，无法反映脊柱角度
4. RGBC 手势对环境光突变敏感，反射基线漂移直接耦合到 TV 信号
5. 被试样本量有限且为非临床人群，外部效度待扩样
6. "隐私友好" = 传感器级数据最小化，非绝对隐私——距离/HR/SpO₂/作息仍属敏感数据

**未来工作**（4 条）：
1. 扩大被试规模，覆盖不同肤色/衣袖/光照
2. RGBC 自适应基线扣除 + 高通滤波（治强光退化）
3. 用户研究验证分级环境光对起身率与打扰感的影响
4. 三通道共享光学前端（分光 / 共享光电二极管）

**参考文献**：22 条（paper.pdf），覆盖 8 个主题：久坐健康 [1-4]、ToF/毫米波手势 [5,8,12]、PPG/血氧 [6,10,11]、视觉手势 [7,9]、WiFi/CSI [13]、压力椅 [14]、隐私 [15]、TinyML [16-20]、办公干预 [21-22]

### 13.3 technical_report.pdf（8.8MB，26 页，2026-06-27，智能装备创新大赛）

**比赛硬性结构**（4 部分）：
1. 场景需求分析报告
2. 技术升级说明报告
3. 实测数据
4. 平台适配性改造说明

**目标用户画像**（表 1）：
| 用户类型 | 特征 | 核心痛点 |
|---|---|---|
| 办公白领 | 日均久坐 8h+ | 姿势不自知 |
| 学生/考研族 | 长时间自习 | 缺时间管理 |
| 程序员 | 深度编码 | 不愿被打断 |
| 远程工作者 | 居家办公 | 缺外部约束 |

**功能需求矩阵**（P0/P1/P3）：
- P0：非接触姿态、番茄钟、LED 视觉反馈
- P1：手势控制、HR、SpO₂、疲劳综合评分
- P3：TFLite 姿态预测（已开发但不用）

**硬件选型**（表 3）：
- AI Board：XIAO ESP32-S3（21×17.5mm，双核 240MHz，双硬件 I²C，WiFi/BLE，USB OTG）
- 显示板：ESP32-C3-DevKitM-1（RISC-V 低功耗，I²C 从机模式）
- VL53L0X（ToF，±3mm，0x29）/ TCS34725（0x29，不同总线）/ MAX30102（PPG，0x57）
- WS2812×60（单线 16M 色）/ SH1106 OLED 128×64 / DS3231（±2ppm）

**竞品对比**（表 4）：
| 功能 | 光合日程AI | Forest | Upright Go | Fitbit |
|---|---|---|---|---|
| 番茄钟 | ✓ | ✓ | × | × |
| 姿态检测 | ✓(ToF) | × | ✓(加速度计) | × |
| 心率/血氧 | ✓(PPG) | × | × | ✓ |
| 手势控制 | ✓(非接触) | × | × | × |
| 无需穿戴 | ✓ | ✓ | × | × |
| 硬件成本 | ¥80-120 | 免费 | ¥600+ | ¥800+ |

**手势算法**（12 帧方差，与 paper.pdf 一致）：
- total < 4000 → 无手势 (-1)
- total > 12000 → 快挥 (-2)
- 4000 ≤ total ≤ 12000 → 评估方向（首尾 C 差 > 800 = 接近 +2 / < -800 = 远离 -3）
- 双击：800ms 内两次快挥 → 触发心率测量
- 慢挥：接近 +20% LED 亮度 / 远离 -20%

**为什么不用 TFLite**（4 条理由）：
1. 规则算法实测 > 95%（手势）/> 98%（姿态）满足产品指标
2. TFLite 运行时需 ~80KB Flash + ~50KB RAM
3. 规则算法确定性强，无硬件加速需求，功耗更低
4. ML 模型保留在代码库，未来可启用

**资源占用**（表 6）：
| 固件 | Flash | RAM |
|---|---|---|
| AI_Board.ino | ~420KB | ~85KB |
| Display_Board.ino | ~210KB | ~45KB |
| gesture_model.h（未用） | ~44KB | — |
| posture_model.h（未用） | ~56KB | — |

**传感器精度预期**（表 7-9，设计验证用，待实测替换）：
- VL53L0X：±3%（短距）~ ±5%（中距）
- MAX30102 HR：±3 bpm / SpO₂ ±2%（静息态）
- TCS34725 手势：双击/无手势 >95%，慢挥 >90%

**功耗预算**（表 11，3.3V 供电）：
| 模块 | 工作 | 待机 |
|---|---|---|
| ESP32-S3 240MHz | ~80mA | ~10mA |
| VL53L0X | ~20mA | ~5µA |
| TCS34725 | ~3mA | ~3µA |
| MAX30102 | ~15mA | ~0.7µA |
| WS2812×60 | ~200mA | 0 |
| ESP32-C3 | ~30mA | ~5mA |
| SH1106 OLED | ~8mA | 0 |
| DS3231 | ~200µA | ~200µA |
| **总计** | **~350-400mA** | **~20mA** |

**平台适配性**（4.3）：
- 引脚重定义：所有外设 `#define` 宏，迁移仅改行
- 传感器替换：VL53L0X → VL53L1X / TCS34725 → APDS-9960（方差算法可复用）/ MAX30102 → MAX30101
- 显示替换：U8g2 支持 200+ 控制器（SH1106 ↔ SSD1306 仅改构造函数）
- 跨平台：ESP32 通用（低）/ ESP32-S3 单芯片合并（中）/ STM32F4（中）/ RP2040（低）/ ATmega328P（高，Flash/RAM 不足）

**6 项未来扩展**（4.4）：
1. BLE 健康数据导出 → 手机 App 长期趋势
2. WiFi 云同步 → 多设备数据聚合
3. 多用户番茄钟同步 → WiFi/BLE mesh
4. 智能家居联动 → Home Assistant/MQTT 调灯色温
5. OTA 更新 TFLite 模型
6. I2S 语音反馈

### 13.4 PDF 之间的关键差异 / 演化痕迹

| 维度 | 策划案 (2026-04) | tech_report (2026-06-27) | paper (2026-08-01) |
|---|---|---|---|
| MCU 架构 | XIAO ESP32C3 **单片** + 微信小程序 | XIAO ESP32-S3 + ESP32-C3 双 MCU + OLED | 同左 |
| 番茄时长 | 未明说（经典 25/5） | **40/5** | 同左 |
| 姿态标签 | 伏案/靠椅/离座 | 伏案/靠椅/离座 | 伏案/**正常**/离席 |
| 手势准确率 | 未量化 | >95% | ~93%（脚注：预期值） |
| 姿态准确率 | 未量化 | >98% | ~96%（脚注：预期值） |
| TFLite 计划 | 4 模型 <15KB | 2 模型已开发未用 | 同左 + 量化对照 |
| SpO₂ 标签 | — | "认知负荷指标" | "疲劳生物标志物" |
| 成本 | ¥180-299 | ¥80-120（硬件） | — |
| 实测数据 | 无 | 标"预期值" | 同样标"预期值，待实测替换" |

**演化逻辑**：策划案是"构想"，tech_report 是"工程实现 + 比赛合规"，paper 是"物理方法 + 学术诚实定位"。**当前最关键缺口**：paper 和 tech_report 都说"实测数据待替换"——这正是 P0。

### 13.5 论文 vs 比赛材料的写法差异（必须区分）

| 维度 | 比赛（technical_report.pdf） | 论文（paper.pdf） |
|---|---|---|
| 语气 | 工程化、产品化、营销化 | 学术化、保守化、限定化 |
| 准确率表述 | ">95% 满足产品指标" | "≈93%…脚注：本节为预期值，最终投稿以实测替换" |
| SpO₂ 定位 | "认知负荷指标" / "疲劳生物标志物" | "工程风险阈值，**并非经临床验证的疲劳判据**" |
| 隐私表述 | "隐私零泄露 / 不上云" | "隐私 by data minimization，**而非绝对隐私**——距离/HR/SpO₂ 仍属敏感数据" |
| 限制条款 | 几乎不提 | 6 条 explicit Limitations |
| 引用 | 0 条 | 22 条 |
| 图风格 | 系统架构图 / 流程图 / 实物照片 | 物理示意 / 混淆矩阵 / Bland-Altman / 对数轴对照 |

**重要**（来自 feedback memory + paper 自述）：**禁止整段复制 competition/technical_report.tex 到 paper/paper.tex**——比赛风格 vs 期刊风格完全不同，混淆会让审稿人立刻拒绝。

### 13.6 已读取 PDF 索引

| PDF | 路径 | 大小 | 页数 | 文本提取 |
|---|---|---|---|---|
| 策划案 | `C:\zhinenti\光合日程AI——基于番茄学习的多模态智能番茄钟策划案.pdf` | 2.4MB | 19 | 已读 |
| 期刊论文 | `C:\zhinenti\paper\paper.pdf` | 2.7MB | 19 | 已读 |
| 期刊论文（带页眉） | `C:\zhinenti\paper\paper光.pdf` | 2.7MB | 19 | 与 paper.pdf 同内容 |
| 比赛技术文档 | `C:\zhinenti\competition\technical_report.pdf` | 8.8MB | 26 | 已读（→ `_tech_report.txt`） |

文本提取副本：`competition/_tech_report.txt`、`paper/_paper.txt`、`paper/_paper光.txt`（pypdf 提取，可被 Read 工具直接读）。
