#include <WiFi.h>
#include <ThingSpeak.h>
#include <DHT.h>

#define DHTPIN 19
#define DHTTYPE DHT22
#define MQ135_PIN 32
#define LED_PIN 23
#define BUZZER_PIN 18

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

WiFiClient client;

unsigned long channelID = YOUR_CAHNNEL_ID;
const char* writeAPIKey = "YOUR_WRITE_API_KEY";

float temperature;
float humidity;
int gasValue;

String airQuality;

void setup() {
  Serial.begin(115200);

  dht.begin();

  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  WiFi.begin(ssid, password);

  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");

  ThingSpeak.begin(client);
}

void loop() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  gasValue = analogRead(MQ135_PIN);

  classifyAir();

  Serial.println("Uploading Data...");

  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  ThingSpeak.setField(3, gasValue);
  ThingSpeak.setField(4, airQuality);

  int response = ThingSpeak.writeFields(channelID, writeAPIKey);

  if (response == 200) {
    Serial.println("Upload Successful");
  } else {
    Serial.print("Upload Failed. Code: ");
    Serial.println(response);
  }

  handleAlerts();

  delay(20000);
}

void classifyAir() {
  if (gasValue < 800)
    airQuality = "Very Good";
  else if (gasValue < 1500)
    airQuality = "Good";
  else if (gasValue < 2200)
    airQuality = "Satisfactory";
  else if (gasValue < 3000)
    airQuality = "Bad";
  else
    airQuality = "Hazardous";
}

void handleAlerts() {
  if (airQuality == "Bad" || airQuality == "Hazardous") {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }
}