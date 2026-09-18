---
name: rec-verify-video
description: 录制智能装备创新大赛验证视频（MP4 ≤100MB, 1920×1080, 无特效）。使用 OBS Studio。
---

# 验证视频录制

为比赛录制 ≤100MB 的 1920×1080 MP4 视频。**比赛要求：仅允许切换镜头，特效禁止**。

## 三段结构（~3 分钟）

| 段 | 时长 | 内容 |
|---|---|---|
| 1. 硬件概览 | 40-60s | 展示组装好的设备，讲解各组件（双MCU、3传感器、LED、OLED） |
| 2. 功能演示 | 60-90s | 手势双击 → 心率测量 → 挥手调亮度 → 姿态三区域切换 → LED 颜色变化 → 番茄钟倒计时 |
| 3. 疲劳检测 | 30s | 模拟长时间伏案 → 疲劳等级 OK → Tired → Rest! → LED 颜色变化 |

## 录制工具

### 方案 A：OBS Studio（推荐）

```bash
# 安装
winget install OBSProject.OBSStudio
```

OBS 设置：
- 分辨率：1920×1080
- 帧率：30 fps
- 编码器：x264 / h264_nvenc
- 码率：6-8 Mbps（控制文件 < 100MB）
- 输出格式：MP4

### 方案 B：Windows Xbox Game Bar

按 `Win+Alt+R` 直接录制。

### 方案 C：ffmpeg + USB 摄像头

```bash
# 列出摄像头
ffmpeg -list_devices true -f dshow -i dummy

# 录制 3 分钟
ffmpeg -f dshow -i video="USB Camera" -t 180 -c:v libx264 -preset medium -crf 23 -r 30 -s 1920x1080 verify.mp4
```

## 后期处理（禁止特效）

```bash
# 仅做切换镜头拼接（不转码重编码，保留质量）
ffmpeg -f concat -safe 0 -i segments.txt -c copy verify.mp4

# 如需重编码（保持简洁）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac verify.mp4
```

## 验证清单

- [ ] 分辨率 = 1920×1080
- [ ] 格式 = MP4
- [ ] 文件大小 < 100MB
- [ ] 时长 2-3 分钟
- [ ] 单一场景内无特效（仅切换可）
- [ ] 三段结构完整

## 输出路径

```bash
/c/zhinenti/competition/verify_video.mp4
```

## 拍摄脚本模板

```
【开场白·20s】
"大家好，这是我们的项目'光合日程AI'。它是基于番茄学习法的多模态桌面助手..."

【硬件概览·40s】
"这是AI主板 XIAO ESP32-S3，负责传感器采集和算法处理；
 这是显示板 ESP32-C3，负责OLED显示和番茄钟；
 这三个传感器是VL53L0X、TCS34725、MAX30102；
 灯条是WS2812，60颗LED..."

【功能演示·90s】
"现在演示手势控制 - 双击触发心率测量..."
"挥手 - 灯光变亮..."
"再挥手 - 灯光变暗..."
"VL53L0X检测到不同距离，LED颜色随之变化..."
"番茄钟开始工作..."

【疲劳检测·30s】
"经过45分钟伏案，心率/血氧/久坐三因子综合判定疲劳等级...
 LED从绿变黄表示Tired..."
```

## 关键设备拍照素材

`C:\zhinenti\65d559d546ecf4de54600c4043ea115b(1).jpg` — OLED 工作状态实物
`C:\zhinenti\3a7edaeec100cb15ee1842138322df20.jpg` — 四大痛点图标

## 如不能用真机拍摄

- 屏幕演示：展示 AI 生成的 3 张产品场景图（`C:\zhinenti\competition\figs\gen_product_*.png`）
- 代码演示：展示 Arduino IDE 关键代码段
- 录屏 + 配音：替代实拍
