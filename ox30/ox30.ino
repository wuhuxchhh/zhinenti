#include <Wire.h>
#include <VL53L0X.h>
VL53L0X sensor;
void setup() {
  Serial.begin(115200);
  Wire.begin(D6, D7);
  sensor.init();
  sensor.setAddress(0x30);
  Serial.println("Address changed to 0x30");
}
void loop() {}