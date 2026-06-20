// 显示板 ESP32-C3-DevKitM-1
// OLED SH1106 SW I2C: GPIO9(SCL)/GPIO8(SDA)
// RTC SW I2C: 同总线 GPIO8/9
// I2C从机: GPIO4(SDA)/GPIO5(SCL) 地址0x08 ← 接收AI主板
#include <Wire.h>
#include <U8g2lib.h>

U8G2_SH1106_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, 9, 8, U8X8_PIN_NONE);

// === RTC 软件I2C GPIO8/9 ===
#define RTC_SDA 8
#define RTC_SCL 9
#define RTC_ADDR 0x68

void rtc_start() {
  pinMode(RTC_SDA, OUTPUT); digitalWrite(RTC_SDA, HIGH);
  pinMode(RTC_SCL, OUTPUT); digitalWrite(RTC_SCL, HIGH);
  delayMicroseconds(5); digitalWrite(RTC_SDA, LOW); delayMicroseconds(5);
  digitalWrite(RTC_SCL, LOW);
}
void rtc_stop() {
  pinMode(RTC_SDA, OUTPUT); digitalWrite(RTC_SDA, LOW);
  pinMode(RTC_SCL, OUTPUT); digitalWrite(RTC_SCL, HIGH);
  delayMicroseconds(5); pinMode(RTC_SDA, INPUT_PULLUP); delayMicroseconds(5);
}
bool rtc_write(uint8_t d) {
  for (int i = 7; i >= 0; i--) {
    digitalWrite(RTC_SDA, (d>>i)&1); delayMicroseconds(2);
    digitalWrite(RTC_SCL, HIGH); delayMicroseconds(5);
    digitalWrite(RTC_SCL, LOW); delayMicroseconds(2);
  }
  pinMode(RTC_SDA, INPUT_PULLUP);
  digitalWrite(RTC_SCL, HIGH); delayMicroseconds(5);
  bool ack = !digitalRead(RTC_SDA);
  digitalWrite(RTC_SCL, LOW); pinMode(RTC_SDA, OUTPUT);
  return ack;
}
uint8_t rtc_read(bool ack) {
  uint8_t d = 0; pinMode(RTC_SDA, INPUT_PULLUP);
  for (int i = 7; i >= 0; i--) {
    digitalWrite(RTC_SCL, HIGH); delayMicroseconds(5);
    if (digitalRead(RTC_SDA)) d |= (1 << i);
    digitalWrite(RTC_SCL, LOW); delayMicroseconds(2);
  }
  pinMode(RTC_SDA, OUTPUT); digitalWrite(RTC_SDA, ack ? LOW : HIGH);
  digitalWrite(RTC_SCL, HIGH); delayMicroseconds(5);
  digitalWrite(RTC_SCL, LOW); return d;
}
uint8_t bcd2dec(uint8_t b) { return (b>>4)*10 + (b&0x0F); }
uint8_t dec2bcd(uint8_t d) { return ((d/10)<<4) | (d%10); }

void writeRTC() {
  rtc_start(); rtc_write(RTC_ADDR << 1); rtc_write(0x00);
  rtc_write(dec2bcd(0));
  int h=((__TIME__[0]-'0')*10+(__TIME__[1]-'0'));
  int m=((__TIME__[3]-'0')*10+(__TIME__[4]-'0'));
  rtc_write(dec2bcd(m)); rtc_write(dec2bcd(h)); rtc_write(1);
  int d=((__DATE__[4]==' '?0:__DATE__[4]-'0')*10+(__DATE__[5]-'0'));
  int mo; const char*M=__DATE__;
  if(M[0]=='J'&&M[2]=='n')mo=1;else if(M[0]=='F')mo=2;else if(M[0]=='M'&&M[2]=='r')mo=3;else if(M[0]=='A'&&M[1]=='p')mo=4;else if(M[0]=='M'&&M[2]=='y')mo=5;else if(M[0]=='J'&&M[2]=='n')mo=6;else if(M[0]=='J'&&M[2]=='l')mo=7;else if(M[0]=='A'&&M[1]=='u')mo=8;else if(M[0]=='S')mo=9;else if(M[0]=='O')mo=10;else if(M[0]=='N')mo=11;else mo=12;
  rtc_write(dec2bcd(d)); rtc_write(dec2bcd(mo)); rtc_write(dec2bcd(26)); rtc_stop();
}

bool rtcOk; uint8_t rtc_h, rtc_m, rtc_s, rtc_d, rtc_mo;
void readRTC() {
  rtc_start(); if (!rtc_write(RTC_ADDR << 1)) { rtc_stop(); return; }
  rtc_write(0x00); rtc_start(); rtc_write((RTC_ADDR << 1) | 1);
  rtc_s = rtc_read(true); rtc_m = rtc_read(true); rtc_h = rtc_read(true);
  rtc_read(true); rtc_d = rtc_read(true); rtc_mo = rtc_read(false);
  rtc_stop();
  rtc_s = bcd2dec(rtc_s & 0x7F); rtc_m = bcd2dec(rtc_m & 0x7F);
  rtc_h = bcd2dec(rtc_h & 0x3F); rtc_d = bcd2dec(rtc_d & 0x3F);
  rtc_mo = bcd2dec(rtc_mo & 0x1F); rtcOk = true;
}

// === I2C从机 接收AI主板 ===
volatile uint8_t rxHR, rxSpO2, rxFat, rxPos, rxGes, rxCmd;
volatile bool newData;

void recvEvent(int n) {
  if (n >= 6) {
    rxHR  = Wire.read(); rxSpO2 = Wire.read();
    rxFat = Wire.read(); rxPos  = Wire.read();
    rxGes = Wire.read(); rxCmd  = Wire.read();
    newData = true;
  } else while (Wire.available()) Wire.read();
}

// === 番茄钟 ===
#define WORK_SEC  (40UL*60)
#define REST_SEC  (5UL*60)
enum { IDLE, WORK, REST } tomato = WORK;
unsigned long tStart, tRemain;
enum { PAGE_TIME, PAGE_ALERT } page = PAGE_TIME;
unsigned long pe;

void setup() {
  u8g2.begin(); u8g2.setFont(u8g2_font_ncenB08_tr);

  readRTC();
  // 只在RTC日期与编译日期不同时校准
  int comp_mo, comp_d;
  const char*M=__DATE__;
  if(M[0]=='J'&&M[2]=='n')comp_mo=1;else if(M[0]=='F')comp_mo=2;else if(M[0]=='M'&&M[2]=='r')comp_mo=3;else if(M[0]=='A'&&M[1]=='p')comp_mo=4;else if(M[0]=='M'&&M[2]=='y')comp_mo=5;else if(M[0]=='J'&&M[2]=='n')comp_mo=6;else if(M[0]=='J'&&M[2]=='l')comp_mo=7;else if(M[0]=='A'&&M[1]=='u')comp_mo=8;else if(M[0]=='S')comp_mo=9;else if(M[0]=='O')comp_mo=10;else if(M[0]=='N')comp_mo=11;else comp_mo=12;
  comp_d=((__DATE__[4]==' '?0:__DATE__[4]-'0')*10+(__DATE__[5]-'0'));
  int comp_h=((__TIME__[0]-'0')*10+(__TIME__[1]-'0'));
  int h_behind = comp_h - rtc_h; // RTC比编译时间落后几小时
  if (!rtcOk || rtc_mo != comp_mo || rtc_d != comp_d || h_behind > 1) {
    writeRTC(); delay(10); readRTC();
  }

  Wire.begin(0x08, 4, 5, 100000); // I2C从机地址0x08, GPIO4/5
  Wire.onReceive(recvEvent);

  tStart = millis(); pe = millis();
}

void loop() {
  readRTC();

  if (newData) {
    newData = false;
    if (rxCmd == 1) { tomato = WORK; tStart = millis(); }
    if (rxCmd == 2) { tomato = IDLE; }
  }

  if (tomato != IDLE) {
    unsigned long total = (tomato == WORK) ? WORK_SEC : REST_SEC;
    unsigned long elap = (millis() - tStart) / 1000;
    if (elap >= total) {
      page = PAGE_ALERT; pe = millis();
      tomato = (tomato == WORK) ? REST : WORK;
      tStart = millis();
    }
    tRemain = total - elap;
  }
  switch (page) { case PAGE_TIME: drawTime(); break; case PAGE_ALERT: drawAlert(); break; }
  delay(200);
}

void drawTime() {
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB18_tr);
  char b[10];
  if (rtcOk) sprintf(b, "%02d:%02d", rtc_h, rtc_m);
  else strcpy(b, "--:--");
  u8g2.drawStr(0, 20, b);
  u8g2.setFont(u8g2_font_ncenB08_tr);
  if (rtcOk) { sprintf(b, "%d/%d", rtc_mo, rtc_d); u8g2.drawStr(80, 12, b); }

  u8g2.setCursor(0, 34);
  u8g2.print(tomato==WORK?"[WORK] ":tomato==REST?"[REST] ":"[IDLE] ");
  if (tomato != IDLE) { unsigned long m = tRemain/60, s = tRemain%60; sprintf(b, "%lu:%02lu", m, s); u8g2.print(b); }

  u8g2.setCursor(0, 48);
  u8g2.print("P:"); u8g2.print(rxPos==0?"Desk":rxPos==1?"Lean":"Away");
  u8g2.print(" F:"); u8g2.print(rxFat==0?"OK":rxFat==1?"Tired":"Rest!");

  u8g2.setCursor(0, 62);
  u8g2.print("HR:"); u8g2.print(rxHR>0?String(rxHR):"--");
  u8g2.print(" SpO2:"); u8g2.print(rxSpO2>0?String(rxSpO2)+"%":"--");
  u8g2.sendBuffer();
}

void drawAlert() {
  if (millis() - pe > 2000) { page = PAGE_TIME; pe = millis(); return; }
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB14_tr);
  u8g2.drawStr(20, 24, "Time's up!");
  u8g2.setFont(u8g2_font_ncenB08_tr);
  u8g2.setCursor(10, 48); u8g2.print(tomato==WORK ? "Work!" : "Rest!");
  u8g2.sendBuffer();
}
