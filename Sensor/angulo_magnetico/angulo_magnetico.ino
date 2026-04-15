#include <Wire.h>

#define AS5600 0x36

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Serial.println("Inicio");
}

void loop() {

  Wire.beginTransmission(AS5600);
  Wire.write(0x0C);   // RAW ANGLE high byte
  byte error = Wire.endTransmission();  // STOP normal

  if (error != 0) {
    Serial.print("Error comunicacion: ");
    Serial.println(error);
    delay(500);
    return;
  }

  Wire.requestFrom(AS5600, 2);

  if (Wire.available() >= 2) {

    uint8_t highByte = Wire.read();
    uint8_t lowByte  = Wire.read();

    uint16_t rawAngle = ((uint16_t)highByte << 8) | lowByte;

    float angleDeg = (rawAngle * 360.0) / 4096.0;

    Serial.print("RAW: ");
    Serial.print(rawAngle);
    Serial.print(" | Grados: ");
    Serial.println(angleDeg);

  } else {
    Serial.println("No datos recibidos");
  }

  delay(200);
}