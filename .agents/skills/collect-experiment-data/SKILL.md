---
name: collect-experiment-data
description: 为「光合日程AI」论文采集真实实验数据的完整协议——手势准确率、姿态、HR/SpO2 对比、功耗、延迟、板间可靠性、RTC 漂移、规则 vs TFLite。含串口日志方案与统计/画图。
---

# 论文实验数据采集协议

产出**可投稿的真实实验数据**（替代比赛文档里的 datasheet 推算值）。每个实验给出：目的、方法、样本量、记录量、统计指标、目标图表。

## 串口日志方案（重要：AI 主板 USB CDC 已损坏）

参见 [[hardware-setup]]：AI 主板 USB CDC 坏了，只能 ROM bootloader 烧录，**无法直接从 AI 板取串口**。方案：

1. **融合输出**（HR/SpO2/疲劳/姿态/手势）：AI 板已通过 I2C 6 字节包发到显示板（`AI_Board.ino:121`）。在**显示板**（ESP32-C3，USB 串口正常，GPIO20/21）加 `Serial.begin(115200)` 并把 `recvEvent` 收到的 6 字节 + `millis()` 时间戳 `Serial.println` 出来，PC 端 pyserial 记录。
2. **AI 板原始信号**（手势 RGBC 12 帧、ToF 距离、dg() 判定）：三选一——
   - (a) 临时扩展板间协议，把原始值也发到显示板转发；
   - (b) AI 板空闲 UART TX 引脚接 USB-TTL 适配器直接打印；
   - (c) 若能修复/绕过 CDC 则直接 `Serial.print`。
   推荐 (a) 做手势实验时临时改协议，实验完再还原。

**PC 端记录器**（pyserial，存 CSV 带时间戳）：
```python
import serial, csv, time
ser = serial.Serial('COM?', 115200, timeout=1)
with open('log.csv','w',newline='') as f:
    w = csv.writer(f)
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line: w.writerow([time.time(), line]); print(line)
```

## 实验清单

### E1 手势识别准确率（主打贡献，最重要）
- 手势类别：双击(触发测量)、慢挥增亮、慢挥减亮、静止/无手势。
- 方法：≥3 名被试，每人每类 ≥20 次 → 每类 ≥60 次。记录 `dg()` 返回值 vs 真实意图。
- **变量：环境光**（暗/室内/明亮/窗边）各重复，验证鲁棒性边界。
- 指标：**混淆矩阵**、每类 precision/recall/F1、总准确率、误触率、双击识别率。
- 图：混淆矩阵热图、不同光照准确率柱状图。

### E2 姿态分类准确率
- 三区：伏案(<400mm)、正常(400-700)、离席(>700)。
- 方法：被试摆位到已知区（卷尺量真实距离作 ground truth），每区 ≥30 次。
- 指标：分类准确率、距离测量误差(mm)、边界附近误分类率。
- 图：真实距离 vs 判定区散点、混淆矩阵。

### E3 心率/血氧 vs 参考仪（关键验证）
- 参考：市售指夹式脉搏血氧仪（或医用级更佳）。
- 方法：≥5 被试，静息态同步测 ≥15 组 HR/SpO2 配对读数。
- 指标：**MAE、RMSE、Bland-Altman 一致性限、Pearson r**。
- 图：Bland-Altman 图、散点+回归线。

### E4 疲劳指数构念效度
- 疲劳无金标准 → 用 **KSS 卡罗林斯卡嗜睡量表自评**或 **PVT 反应时**作对照。
- 方法：被试连续伏案，每 15min 记录系统疲劳等级 + KSS 自评，共 ≥60min。
- 指标：系统等级与 KSS 的 Spearman 相关；诚实说明是启发式而非临床。
- 图：疲劳等级 & KSS 随时间曲线。

### E5 规则 vs TFLite 对比（支撑"弃 ML 选规则"论点）
- 用同一测试集跑规则算法 vs `gesture_model.h`/`posture_model.h` TFLite 模型。
- 指标表：准确率、推理延迟(ms)、flash 占用(KB)、RAM(KB)。用真实测量填。
- 图：对比条形图或表格。

### E6 板间通信可靠性
- 方法：连续运行 ≥1h，显示板计数收到包 vs 应收包(1Hz)。
- 指标：丢包率、字段错误率。

### E7 功耗
- USB 功率计/万用表测：待机、测量态、LED 满亮各功耗；估续航（若电池）。
- 图：各状态功耗条形图。

### E8 RTC 漂移
- 与 NTP/手机对时，记录 24h（或更久）漂移秒数，折算 ppm。

### E9 端到端延迟
- 手势触发 → LED/OLED 响应的时间（视频逐帧或代码打点）。

## 统计与画图约定

- 报告 mean ± SD，配对比较用配对 t 检验或 Wilcoxon，相关用 Pearson/Spearman，标注 n 和 p。
- 图用 matplotlib，风格follCLAUDE.md，但**论文图英文标注**（投英文刊时），dpi≥300，存 `paper/figs/`。
- 原始 CSV 存 `paper/data/`，画图脚本存 `paper/analysis/`，保证可复现。

## 采集前检查
- [ ] 显示板加了串口日志并验证 PC 能收到
- [ ] 手势实验临时协议改好（E1）
- [ ] 参考血氧仪就位（E3）
- [ ] 被试知情、记录被试编号（匿名）
- [ ] 每个实验的 CSV 带绝对时间戳
