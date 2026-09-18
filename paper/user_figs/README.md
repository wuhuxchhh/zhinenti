# user_figs/ — 用户确认保留的论文图

**生成日期：** 2026-07-15
**来源：** `paper.pdf`（用户在 PDF 编辑器中修改/新增后导出）

## 对应关系（按出现页码 + 尺寸匹配）

| 文件 | 页 | 尺寸 | 论文中的图 |
|---|---|---|---|
| p04_x439_d42d826632.png | 4 | 1227×721 | fig_architecture.png（**用户修改/替换版**，源图被覆盖） |
| p04_x440_2d1849f698.png | 4 | 1227×664 | fig_gesture_flowchart.png（**用户修改/替换版**） |
| p05_x442_123f9a7b3b.png | 5 | 1133×666 | fig_i2c_topology.png（**用户修改/替换版**） |
| p06_x444_3809dac97b.png | 6 | 1040×1144 | fig_posture_zones.png（**用户修改/替换版**） |
| p06_x445_c379e50cb0.png | 6 | 1142×931 | fig_fatigue_curve.png（**用户修改/替换版**） |
| p07_x447_81ab3c8c42.png | 7 | 864×440 | fig_led_feedback.png（**用户修改/替换版**） |
| p07_x86_10cf4f4df3.png  | 7 | 3060×1517 | fig_posture_zones.png / 旧版本（与 p06 同名） |
| p08_x94_d9cb9d1543.png | 8 | 2781×1796 | fig_fatigue_curve.png（高清版） |
| p08_x97_84974c2f2b.png | 8 | 3060×1657 | fig_led_feedback.png（高清版） |
| p09_x103_7ab492313c.png | 9 | 3060×1237 | fig_data_protocol.png |
| p10_x115_775bd133f6.png | 10 | 1789×1530 | fig_gesture_confusion.png |
| p10_x117_7b5882589a.png | 10 | 1888×1230 | fig_gesture_lighting.png |
| p11_x123_a0e2a90f2f.png | 11 | 3063×1292 | fig_posture_eval.png |
| p11_x126_2d050ac8ca.png | 11 | 3268×1293 | fig_bland_altman.png |
| p12_x132_e7beb5a2d0.png | 12 | 2066×1261 | fig_fatigue_kss.png |
| p13_x139_9eceaf983f.png | 13 | 2124×1290 | fig_rule_vs_ml.png |

## 注意

- p07/p08 各有**两份**：高分辨率版（3060 宽）来自源图，被 PDF 重编码后尺寸未变；另一份（p07_x447、p08_x94）尺寸明显不同，**很可能是用户在 PDF 中替换/重排后的版本**，以这一份为准。
- 这 16 张图请勿重生成。如需修改论文中的某张图，**先确认你要改的图对应这里哪一份，再决定是覆盖源图还是直接编辑本目录里的备份**。
- `gen_paper_figs.py` 仅生成实验结果图（fig_gesture_confusion / fig_gesture_lighting / fig_posture_eval / fig_bland_altman / fig_fatigue_kss / fig_rule_vs_ml），不涉及本目录的图。
