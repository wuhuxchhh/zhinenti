---
name: gen-tech-figs
description: 重新生成技术文档中的 matplotlib 图表。统一中文 SimHei 字体、浅色圆角盒风格、dpi=180。脚本：gen_all_figs_zh.py
---

# 技术图表统一生成

执行 `C:\zhinenti\competition\gen_all_figs_zh.py` 重新生成全部 14 张技术图。

## 使用方法

```bash
# 生成全部 14 张
/c/Users/ASUS/AppData/Local/Programs/Python/Python313/python.exe /c/zhinenti/competition/gen_all_figs_zh.py

# 或用 shell 函数
genfigs
```

## 当前 14 张图清单

| # | 文件名 | 内容 |
|---|---|---|
| 1 | fig_architecture.png | 双MCU系统架构总览 |
| 2 | fig_gesture_flowchart.png | 手势检测算法流程 |
| 3 | fig_fatigue_curve.png | 疲劳生物标志物曲线 |
| 4 | fig_i2c_topology.png | I2C总线拓扑 |
| 5 | fig_pomodoro_state.png | 番茄钟状态机 |
| 6 | fig_posture_zones.png | 姿态检测三区域 |
| 7 | fig_data_protocol.png | 板间I2C通信协议 |
| 8 | fig_led_feedback.png | LED色彩反馈系统 |
| 9 | fig_wiring.png | 硬件接线图 |
| 10 | fig_startup_sequence.png | 启动自检LED序列 |
| 11 | fig_rtc_timing.png | RTC软件I2C位带时序 |
| 12 | fig_resource_usage.png | 资源占用柱状图 |
| 13 | fig_dataflow.png | 数据流时间线 |
| 14 | fig_edge_vs_cloud.png | 端云架构对比 |

## 风格约束（已硬编码在脚本中）

- 字体：SimHei（中文）
- dpi=180
- 字号：标题15pt / 框标题13pt / 正文11pt / 注释9pt
- 色板：`#FF8A95` 粉 / `#A8E0A0` 绿 / `#A0D8F0` 蓝 / `#FFD8A8` 橙
- 禁用字符：`²` 和 `↔`（SimHei 缺失）

## 修改流程

1. 编辑 `C:\zhinenti\competition\gen_all_figs_zh.py`
2. 运行 `genfigs` 重生成
3. 用 Read 工具查看 1-2 张图确认效果
4. 编译 PDF：`techpdf`
