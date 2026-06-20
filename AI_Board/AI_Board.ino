// 光合日程 AI - 最终版
// LED=D6, Wire(SDA/SCL)=D8/D9(VL53L0X), Wire1=D1/D2(TCS34725+MAX30102)
#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#include <VL53L0X.h>
#include <Adafruit_TCS34725.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"

#define LP 6   // D6
#define N  60
Adafruit_NeoPixel strip(N, LP, NEO_GRB + NEO_KHZ800);

VL53L0X tof;
Adafruit_TCS34725 tcs;
MAX30105 ps;
bool mOk, tOk, cOk;

void lf(int r,int g,int b){ strip.fill(strip.Color(r,g,b)); strip.show(); }

#define PL 15
float pb[PL]; int pi,posture,lastP=-1;
unsigned long pms,pmin;

#define GL 12
uint16_t gR[GL],gG[GL],gB[GL],gC[GL]; int gi; bool gA;

bool lon=true; int br=150;
bool hb; int si; uint32_t iB[100],rB[100];
int32_t hr,sp; int8_t vh,vs; int fat;

void setup(){
  strip.begin(); strip.setBrightness(80);
  lf(255,0,0); delay(600); lf(0,255,0); delay(600); lf(0,0,255); delay(600); // RGB启动指示灯
  lf(255,255,255); delay(400); // 白

  Wire.begin(8,9);   // VL53L0X 独占 D8(SDA)/D9(SCL)
  Wire1.begin(1,2);  // TCS34725 + MAX30102 D1/D2

  // 紫 = VL53L0X (Pololu库, 独占D8/D9)
  lf(255,0,255); delay(300);
  tof.setBus(&Wire);
  if(tof.init()){
    tof.startContinuous();
    tOk=true;
  }

  // 青 = MAX30102 (D1/D2)
  lf(0,255,255); delay(300);
  if(ps.begin(Wire1,I2C_SPEED_FAST)){ ps.setup(60,4,2,100,411,4096); mOk=true; }

  // 蓝 = TCS34725 (D1/D2, 地址0x29不冲突)
  lf(0,0,255); delay(300);
  if(tcs.begin(TCS34725_ADDRESS, &Wire1)){
    tcs.setIntegrationTime(TCS34725_INTEGRATIONTIME_24MS);
    tcs.setGain(TCS34725_GAIN_16X);
    cOk=true;
  }

  int ok=tOk+cOk+mOk;
  if(ok==3) lf(0,255,0); else if(ok>0) lf(255,160,0); else lf(255,0,0);
  delay(2000);

  for(int i=0;i<3;i++){ lf(tOk?0:255, tOk?255:0, 0); delay(250); lf(0,0,0); delay(250); }
  lf(255,255,255); delay(400);
  for(int i=0;i<3;i++){ lf(cOk?0:255, cOk?255:0, 0); delay(250); lf(0,0,0); delay(250); }
  lf(255,255,255); delay(400);
  for(int i=0;i<3;i++){ lf(mOk?0:255, mOk?255:0, 0); delay(250); lf(0,0,0); delay(250); }

  lf(255,220,180); gA=true;
}

void loop(){
  if(tOk){
    uint16_t d=tof.readRangeContinuousMillimeters();
    if(tof.timeoutOccurred()||d==65535) d=800;
    if(pi<PL) pb[pi++]=(float)d;

    if(pi>=PL){
      pi=0; float a=0; for(int i=0;i<PL;i++) a+=pb[i]; a/=PL;
      if(a<400) posture=0; else if(a<700) posture=1; else posture=2;
      if(posture!=lastP){ pms=millis(); lastP=posture; }
      pmin=(posture==0)?(millis()-pms)/60000:0;
      upLED();
    }
  }

  // 手势检测
  if(cOk){
    uint16_t r,g,b,c;
    tcs.getRawData(&r,&g,&b,&c);
    if(gi<GL){ gR[gi]=r; gG[gi]=g; gB[gi]=b; gC[gi]=c; gi++; }
    if(gi>=GL){ int g=dg(); hg(g); gi=0; }
  }

  if(hb&&mOk){
    ps.check();
    while(ps.available()&&si<100){ iB[si]=ps.getIR(); rB[si]=ps.getRed(); ps.nextSample(); si++; }
    lf(0,0,200);
    if(si>=100){ maxim_heart_rate_and_oxygen_saturation(iB,100,rB,&sp,&vs,&hr,&vh); hb=false; si=0;
      int sc=0;
      if(vh&&hr>85) sc++; if(vs&&sp<95) sc++;
      if(posture==0&&pmin>=45) sc++;
      int f=(sc==0)?0:(sc==1)?1:2;
      for(int i=0;i<8;i++){
        if(f==0) lf(0,255,0); else if(f==1) lf(255,255,0); else lf(255,0,0);
        delay(250); lf(0,0,0); delay(250);
      }
      upLED(); }
  }

  int sc=0;
  if(vh&&hr>85) sc++; if(vs&&sp<95) sc++;
  if(posture==0&&pmin>=45) sc++;
  fat=(sc==0)?0:(sc==1)?1:2;

  // 发送数据到显示板 (I2C从机 0x08)
  static unsigned long ls;
  if(millis()-ls>1000){
    ls=millis();
    Wire1.beginTransmission(0x08);
    Wire1.write((uint8_t)(vh?hr:0)); // HR
    Wire1.write((uint8_t)(vs?sp:0)); // SpO2
    Wire1.write((uint8_t)fat);       // 疲劳
    Wire1.write((uint8_t)posture);   // 姿态
    Wire1.write((uint8_t)0);         // 手势(预留)
    Wire1.write((uint8_t)0);         // 番茄钟命令
    Wire1.endTransmission();
  }

  delay(10);
}

int dg(){
  float rv,gv,bv,cv; rv=gv=bv=cv=0;
  for(int i=1;i<GL;i++){ rv+=abs((int)gR[i]-(int)gR[i-1]); gv+=abs((int)gG[i]-(int)gG[i-1]); bv+=abs((int)gB[i]-(int)gB[i-1]); cv+=abs((int)gC[i]-(int)gC[i-1]); }
  float tv=rv+gv+bv+cv, cf=gC[0]+gC[1]+gC[2], cl=gC[GL-3]+gC[GL-2]+gC[GL-1];
  if(tv<4000) return -1; if(tv>12000) return -2;
  if(tv>6000){ if(cl-cf>800) return 2; if(cf-cl>800) return 3; }
  return -1;
}

void hg(int g){
  static unsigned long ft; // 第一次快速手势的时间
  if(g==-2){ // 快速挥手
    unsigned long n=millis();
    if(n-ft<800&&ft>0){ // 双击! 800ms内两次快挥→触发测量
      ft=0;
      lf(0,0,255); delay(150); // 蓝灯确认
      if(!hb&&mOk&&lon){ hb=true; si=0; memset(iB,0,sizeof(iB)); memset(rB,0,sizeof(rB)); }
    }else{
      ft=n; // 记录第一次
      lf(255,255,0); delay(100); upLED(); // 黄灯提示=第一次,等待第二次
    }
  }else if(g==2&&lon){ // 慢挥增亮
    lf(0,255,0); delay(100);
    br=min(255,br+20); strip.setBrightness(br); strip.show();
  }
  else if(g==3&&lon){ // 慢挥减亮
    lf(255,0,0); delay(100);
    br=max(0,br-20); strip.setBrightness(br); strip.show();
  }
}

void upLED(){
  if(!lon) return;
  if(!tOk){
    lf(100,100,100); // 无姿态传感器 = 暗白
    return;
  }
  if(posture==0)      lf(255,220,180);
  else if(posture==1) lf(180,200,255);
  else                lf(80,80,80);
}
