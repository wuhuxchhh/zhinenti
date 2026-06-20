#include <Adafruit_NeoPixel.h>
#define LP 6
#define N  60
Adafruit_NeoPixel strip(N, LP, NEO_GRB + NEO_KHZ800);
void setup(){
  strip.begin(); strip.setBrightness(255);
  strip.fill(strip.Color(255,255,255)); strip.show();
}
void loop(){}
