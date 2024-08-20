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

  TelnetStream.begin();
  Serial.println("Telnet-Server gestartet. Verbinde dich mit einem Telnet-Client.");
  TelnetStream.print("Verfügbare Zeichen: 't' 'w' 'a' 's' 'd' 'x'");

  test();
}

void loop() {
  if (TelnetStream.available()) {
    char incomingChar = TelnetStream.read();
    switch (incomingChar) {
      case 't':
        stop(); 
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: T");
        break;
      case 'w':
        stop();
        Serial.println(incomingChar);
        digitalWrite(12,HIGH);
        digitalWrite(14,HIGH);        
        TelnetStream.println("Test erfolgreich: w");
        delay(500);
        break;
      case 'a':
        stop();
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: a");
        digitalWrite(14,HIGH); 
        delay(500);       
        break;       
      case 's':
        stop();
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: s");
        digitalWrite(27,HIGH);
        digitalWrite(26,HIGH);
        delay(500);
        break;       
      case 'd':
        stop();
        Serial.println(incomingChar);
        TelnetStream.println("Test erfolgreich: d");
        digitalWrite(12,HIGH);
        delay(500);
        break;
      case 'x':
        Serial.println(incomingChar);
        Serial.print("  -> Case: x");
        digitalWrite(12,LOW);
        digitalWrite(14,LOW);
        digitalWrite(27,LOW);
        digitalWrite(26,LOW);
    }
  }
}

//void key_pressed(int i) {
//  // TelnetStream.println("Starting: " + i);
//  digitalWrite(i,HIGH);
//  delay(1000);
//  digitalWrite(i,LOW);
//  }

void stop() {
  Serial.println("stopping  -> Case: stop");
  digitalWrite(12,LOW);
  digitalWrite(14,LOW);
  digitalWrite(27,LOW);
  digitalWrite(26,LOW);
  }

void test() {
  Serial.println("TESTING...");
  digitalWrite(12,HIGH);
  digitalWrite(14,HIGH);
  digitalWrite(27,HIGH);
  digitalWrite(26,HIGH);
  delay(500);
  digitalWrite(12,LOW);
  digitalWrite(14,LOW);
  digitalWrite(27,LOW);
  digitalWrite(26,LOW);
  }
 
