#include <ArduinoJson.h>
#include <ArduinoJson.hpp>

#include <DHT.h>
#define Type DHT11
int sensePin=2;
int setTime=2000;
int dt=2000;

DHT HT(sensePin,Type);
float humidity;
float tempC;
float tempF;
JsonDocument doc;

void setup() {
  Serial.begin(9600);
  HT.begin();
  delay(setTime);
}

void loop() {
  humidity=HT.readHumidity();
  tempC=HT.readTemperature();
  tempF=HT.readTemperature(true);
  doc["humidity"] = humidity;
  doc["temp_c"] = tempC;
  doc["temp_f"] = tempF;
  serializeJson(doc, Serial);
  Serial.println();
  delay(dt);
}
