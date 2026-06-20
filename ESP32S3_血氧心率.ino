#include <Wire.h>
#include <Adafruit_VL53L0X.h>
#include <Adafruit_TCS34725.h>
#include <FastLED.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

#include "posture_model.h"
#include "gesture_model.h"

// ===================== 引脚定义 (XIAO ESP32S3) =====================
#define LED_PIN     4
#define NUM_LEDS    4
#define I2C_SDA     6
#define I2C_SCL     7

CRGB leds[NUM_LEDS];

Adafruit_VL53L0X tof;
Adafruit_TCS34725 tcs;
MAX30105 particleSensor;

// ===================== 姿态检测 =====================
#define SEQUENCE_LEN 50
float pose_buffer[SEQUENCE_LEN];
int buffer_idx = 0;
int posture = 0;
bool tomato_running = false;

// ===================== 血氧心率 =====================
#define SPO2_BUF_LEN 100
uint32_t irBuffer[SPO2_BUF_LEN];
uint32_t redBuffer[SPO2_BUF_LEN];
int spo2_idx = 0;
bool spo2_ready = false;
int32_t spo2 = 0;
int8_t  validSPO2 = 0;
int32_t heartRate = 0;
int8_t  validHeartRate = 0;
bool    max30105_ok = false;   // 传感器是否初始化成功
uint8_t shift_count = 0;

void setup() {
  delay(500);
  Serial.begin(115200);
  Wire.begin(I2C_SDA, I2C_SCL);

  // ---- 灯光 ----
  FastLED.addLeds<WS2812, LED_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(100);
  fill_solid(leds, NUM_LEDS, CRGB(255, 0, 0));
  FastLED.show();

  // ---- 原有传感器 ----
  tof.begin();
  tcs.begin();

  // ---- MAX30105 初始化 ----
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("⚠ MAX30105 未找到，血氧心率功能不可用");
  } else {
    particleSensor.setup(60, 4, 2, 100, 411, 4096);
    max30105_ok = true;
    Serial.println("✅ MAX30105 初始化成功");
  }

  Serial.println("✅ 系统就绪");
}

void loop() {
  // ===================== 1. 距离采样 =====================
  uint16_t dist = tof.readRange();
  if (dist == 65535) dist = 800;

  if (buffer_idx < SEQUENCE_LEN) {
    pose_buffer[buffer_idx++] = dist;
  }

  // ===================== 2. 血氧心率采样 =====================
  if (max30105_ok) {
    particleSensor.check();
    int reads = 0;
    while (particleSensor.available() && reads < 10) {
      uint32_t ir  = particleSensor.getIR();
      uint32_t red = particleSensor.getRed();
      particleSensor.nextSample();
      reads++;

      if (!spo2_ready) {
        irBuffer[spo2_idx]  = ir;
        redBuffer[spo2_idx] = red;
        spo2_idx++;
        if (spo2_idx >= SPO2_BUF_LEN) {
          spo2_idx = 0;
          spo2_ready = true;
          maxim_heart_rate_and_oxygen_saturation(
            irBuffer, SPO2_BUF_LEN, redBuffer,
            &spo2, &validSPO2, &heartRate, &validHeartRate
          );
        }
      } else {
        if (shift_count == 0) {
          for (int i = 25; i < SPO2_BUF_LEN; i++) {
            irBuffer[i - 25]  = irBuffer[i];
            redBuffer[i - 25] = redBuffer[i];
          }
        }
        irBuffer[75 + shift_count]  = ir;
        redBuffer[75 + shift_count] = red;
        shift_count++;

        if (shift_count >= 25) {
          shift_count = 0;
          maxim_heart_rate_and_oxygen_saturation(
            irBuffer, SPO2_BUF_LEN, redBuffer,
            &spo2, &validSPO2, &heartRate, &validHeartRate
          );
        }
      }
    }
  }

  // ===================== 3. 姿态判断 =====================
  if (buffer_idx >= SEQUENCE_LEN) {
    buffer_idx = 0;
    float avg = 0;
    for (int i = 0; i < SEQUENCE_LEN; i++) avg += pose_buffer[i];
    avg /= SEQUENCE_LEN;

    if (avg < 400)      posture = 0;
    else if (avg < 700) posture = 1;
    else                posture = 2;
  }

  // ===================== 4. 番茄钟 =====================
  if (posture == 0 && !tomato_running) {
    tomato_running = true;
    Serial.println("🍅 番茄钟启动");
  }
  if (posture == 2 && tomato_running) {
    tomato_running = false;
    Serial.println("🛑 番茄钟暂停");
  }

  // ===================== 5. 灯光 =====================
  if (posture == 0)      fill_solid(leds, NUM_LEDS, CRGB(255, 220, 180));
  else if (posture == 1) fill_solid(leds, NUM_LEDS, CRGB(180, 200, 255));
  else                   fill_solid(leds, NUM_LEDS, CRGB(80, 80, 80));
  FastLED.show();

  // ===================== 6. 串口输出 =====================
  Serial.print("📏 ");
  Serial.print(dist);
  Serial.print("mm | 🤖 ");
  Serial.print(posture == 0 ? "伏案" : posture == 1 ? "靠椅" : "离座");

  // 血氧心率输出
  Serial.print(" | ❤️ HR:");
  if (validHeartRate) {
    Serial.print(heartRate);
  } else {
    Serial.print("--");
  }
  Serial.print("bpm | 💉 SpO2:");
  if (validSPO2) {
    Serial.print(spo2);
    Serial.print("%");
  } else {
    Serial.print("--");
  }

  Serial.println();
  delay(50);
}
