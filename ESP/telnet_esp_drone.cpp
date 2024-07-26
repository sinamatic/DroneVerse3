#include <WiFi.h>
#include <TelnetStream.h>

const char ssid[] = "free_internet";    // WLAN-SSID
char pass[] = "bjornbonsai";      // WLAN-Passwort


void setup() {

  pinMode(12, OUTPUT); //BL -> B1
  pinMode(14, OUTPUT); //BR -> A3
  pinMode(27, OUTPUT); //FL -> B4
  pinMode(26, OUTPUT); //FR -> A2

  // B1, A3, B4, A2
  // Transitor: GPIO, Strom+, Strom-(also Motor dann GND)
  // Alle GND in "-"Leiste dann in ESP UND die Akkus zurück

  Serial.begin(115200);

  Serial.print("Verbindung mit WLAN-Netzwerk (SSID): ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  
  Serial.println("");
  Serial.println("Verbunden mit WLAN-Netzwerk.");
  Serial.print("IP-Adresse des ESP32: ");
  Serial.println(WiFi.localIP());

  test();

  TelnetStream.begin();
  Serial.println("Telnet-Server gestartet. Verbinde dich mit einem Telnet-Client.");
}

void loop() {
  if (TelnetStream.available()) {
    char incomingChar = TelnetStream.read();
    switch (incomingChar) {
//      case 'R':
//        // Serial.println("Detected char: ");
//        // Serial.print(incomingChar);
//        TelnetStream.println("Neustart des ESP32...");
//        TelnetStream.stop();
//        delay(100);
//        // ESP.restart();
//        break;
//      case 'C':
//        Serial.println("Detected char: ");
//        Serial.print(incomingChar);
//        TelnetStream.println("Auf Wiedersehen!");
//        TelnetStream.stop();
//        break;
      case 'T':
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: T");
        break;
      case 'w':
        Serial.println(incomingChar);
        vor();
        TelnetStream.println("Test erfolgreich: w");
        break;
      case 'a':
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: a");
        left();
        break;       
      case 's':
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: s");
        hoch();
        break;       
      case 'd':
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: d");
        right();
        break;
    }
  }
}

void key_pressed(int i) {
  // TelnetStream.println("Starting: " + i);
  digitalWrite(i,HIGH);
  delay(1000);
  digitalWrite(i,LOW);
  }

// TASTE: W
void vor () {
  digitalWrite(12,HIGH);
  digitalWrite(14,HIGH);
  delay(1000);
  digitalWrite(12,LOW);
  digitalWrite(14,LOW);
  }

//TASTE: A
void left() {
  digitalWrite(14,HIGH);
  delay(1000);
  digitalWrite(14,LOW);
  }

//TASTE: S
void hoch() {
  digitalWrite(27,HIGH);
  digitalWrite(26,HIGH);
  delay(1000);
  digitalWrite(27,LOW);
  digitalWrite(26,LOW);
  }

//TASTE: D
void right() {
  digitalWrite(12,HIGH);
  delay(1000);
  digitalWrite(12,LOW);
  }

void test() {
  Serial.println("TESTING...");
  digitalWrite(12,HIGH);
  digitalWrite(14,HIGH);
  digitalWrite(27,HIGH);
  digitalWrite(26,HIGH);
  delay(1000);
  digitalWrite(12,LOW);
  digitalWrite(14,LOW);
  digitalWrite(27,LOW);
  digitalWrite(26,LOW);
  }
 