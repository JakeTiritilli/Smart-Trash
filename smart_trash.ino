#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22

const char* ssid     = "UCInet Mobile Access";
const char* password = "";
//const char* ssid     = "VDCN-Resident";
//const char* password = "AC86fm!6";

const int TRIG_PIN = 12;
const int ECHO_PIN = 13;

// Anything over 400 cm (23200 us pulse) is "out of range"
const unsigned int MAX_DIST = 23200;

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(115200);
  delay(10);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // The Trigger pin will tell the sensor to range find
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  dht.begin();
}

void loop()
{
  delay(5000);

  float dist = getUltraSonicDist();

  float temp = getDhtTemp();
  if (isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  sendHttpRequest(dist, temp);
}

void sendHttpRequest(float dist, float temp)
{
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["dist"] = dist;
  root["temp"] = temp;

  char jsonMsgBuffer[200];
  root.printTo(jsonMsgBuffer, sizeof(jsonMsgBuffer));
  
  HTTPClient http;
  Serial.print("[HTTP] begin...\n");
  http.begin("http://169.234.43.2:5000"); // Change to name of proper URL
  http.addHeader("Content-Type", "application/json");

  Serial.print("[HTTP] POST...\n");
  // start connection and send HTTP header
  int httpCode = http.POST(jsonMsgBuffer);
  String payload = http.getString();
  Serial.println(httpCode);
  Serial.println(payload);
  
  http.end();
}

float getUltraSonicDist()
{
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  // Hold the trigger pin high for at least 10 us
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure how long the echo pin was held high (pulse width)
  // Note: the micros() counter will overflow after ~70 min
  unsigned long pulse_width = pulseIn(ECHO_PIN, HIGH);

  float inches = pulse_width / 148.0;

  // Print out results
  if ( pulse_width > MAX_DIST ) {
    Serial.println("Out of range");
  } else {
    Serial.print(inches);
    Serial.println(" in");
  }
  return inches;
}

float getDhtTemp()
{
  // Read temperature in Fahrenheit
  float temp = dht.readTemperature(true);
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print(" *F\n");
  return temp;
}

