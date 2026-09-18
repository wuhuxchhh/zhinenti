---
name: dashscope-image-gen
description: 阿里云DashScope通义万相AI画图，支持文生图、图生图、图像编辑。API key 从 DASHSCOPE_API_KEY 环境变量读取。
---

# DashScope 通义万相 AI 画图

调用阿里云百炼 DashScope API 进行 AI 图像生成。API Key 存储在 `DASHSCOPE_API_KEY` 环境变量中。

## 可用模型

### 文生图 (Text-to-Image)

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| `qwen-image-max` | 最新旗舰，综合最强 **推荐** | 高质量产品图、场景图 |
| `qwen-image-plus` | 性价比之选 | 日常配图 |
| `wan2.2-t2i-plus` | Wan 2.2 文生图 | 写实风格 |
| `wanx2.1-t2i-turbo` | 速度优先 | 快速迭代 |
| `wan2.7-image` | Wan 2.7 最新 | 极致画质 |
| `wan2.7-image-pro` | Wan 2.7 Pro | 专业级 |

### 图生图 / 图像编辑

| 模型 | 说明 |
|------|------|
| `qwen-image-edit-plus` | 图像编辑 |
| `qwen-image-edit-max` | 图像编辑旗舰 |
| `wan2.5-i2i-preview` | 图生图 |

### 视频生成（备选）

| 模型 | 说明 |
|------|------|
| `wan2.7-t2v` | 文生视频 |
| `wan2.7-i2v` | 图生视频 |

## 文生图调用

```python
import requests, os, time

api_key = os.environ["DASHSCOPE_API_KEY"]

def generate_image(prompt, model="qwen-image-max", size="1024*1024"):
    resp = requests.post(
        "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "input": {
                "messages": [{
                    "role": "user",
                    "content": [{"text": prompt}]
                }]
            },
            "parameters": {"size": size}
        }
    )
    data = resp.json()
    if resp.status_code == 200:
        for choice in data["output"]["choices"]:
            for item in choice["message"]["content"]:
                if "image" in item:
                    return item["image"]  # OSS signed URL
    else:
        raise Exception(f"API error: {data.get('message', resp.text)}")

# 示例：生成产品渲染图
url = generate_image("A modern smart desk timer device with colorful LED ring, sitting on a white desk next to a monitor, clean lighting")
print(url)
```

## 下载生成的图片

```python
import requests

def download_image(url, filepath):
    resp = requests.get(url)
    if resp.status_code == 200 and len(resp.content) > 1000:
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return True
    return False
```

## 批量生图（用于文档配图）

```python
scenes = [
    "System architecture diagram of a dual-MCU IoT pomodoro timer device, showing ESP32-S3 and ESP32-C3 connected via I2C, clean technical illustration style",
    "Hand gesture controlling LED lights on a smart desk timer, non-contact interaction, sleek modern design",
    "Fatigue monitoring dashboard concept: heart rate, SpO2, posture data displayed with color-coded LED feedback",
]

for i, prompt in enumerate(scenes):
    url = generate_image(prompt, model="qwen-image-max", size="1024*1024")
    # url 有效期有限，尽快下载
    download_image(url, f"competition/figs/gen_scene_{i+1}.png")
    time.sleep(2)
```

## 文本模型（同 Key 可用）

同一 Key 也可调用通义千问文本模型：

```python
resp = requests.post(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": "..."}]
    }
)
print(resp.json()["choices"][0]["message"]["content"])
```

## 注意事项

- 图片 URL 有有效期（OSS 签名过期），生成后尽快下载
- `qwen-image-max` 单张生成约 15-30 秒
- 尺寸支持：`1024*1024`, `1280*720`, `720*1280` 等
- API Key 从 `DASHSCOPE_API_KEY` 环境变量读取，已配置在 `.claude/settings.local.json`
