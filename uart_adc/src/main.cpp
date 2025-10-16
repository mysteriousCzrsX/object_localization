#include <Arduino.h>

void setup() {
  Serial.begin(9600);
  
}

void loop() {
  uint16_t pot1 = analogRead(A0);
  uint16_t pot2 = analogRead(A1);
  Serial.print(pot1);
  Serial.print(",");
  Serial.println(pot2);
  delay(1000);
}
