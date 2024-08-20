/*
 * Author: Tobias Schwarz
 * This ESP32 code is created by esp32io.com
 *
 * This ESP32 code is released in the public domain
 *
 * For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-controls-led-via-web
 */

// change this to platformio project for usage in vsc or use arduino ide
// #include <Arduino.h>

#include <ESPAsyncWebServer.h>
#include <WiFi.h>

#define LED_PIN_1 18 // ESP32 pin GPIO18 connected to LED
#define LED_PIN_2 19
#define LED_PIN_3 16
#define LED_PIN_4 17

const char *ssid = "free_internet";   // CHANGE IT
const char *password = "bjornbonsai"; // CHANGE IT

AsyncWebServer server(80);

int LED_state = LOW;

String getHTML()
{
  String html = "<!DOCTYPE HTML>";
  html += "<html>";
  html += "<head>";
  html += "<link rel='icon' href='data:,'>";
  html += "</head>";
  //  html += "<p>LED state: <span style='color: red;'>";
  //
  //  if (LED_state == LOW)
  //    html += "OFF";
  //  else
  //    html += "ON";
  //
  //  html += "</span></p>";

  html += "<a href='/led1/on'>Turn ON_1</a>";
  html += "<br><br>";
  html += "<a href='/led1/off'>Turn OFF_1</a>";
  html += "</html>";

  html += "</span></p>";
  html += "<a href='/led2/on'>Turn ON_2</a>";
  html += "<br><br>";
  html += "<a href='/led2/off'>Turn OFF_2</a>";
  html += "</html>";

  html += "</span></p>";
  html += "<a href='/led3/on'>Turn ON_3</a>";
  html += "<br><br>";
  html += "<a href='/led3/off'>Turn OFF_3</a>";
  html += "</html>";

  html += "</span></p>";
  html += "<a href='/led4/on'>Turn ON_4</a>";
  html += "<br><br>";
  html += "<a href='/led4/off'>Turn OFF_4</a>";
  html += "</html>";

  html += "</span></p><br><br><br>";
  html += "<a href='/led_all/on'>Turn ON_ALL</a>";
  html += "<br><br>";
  html += "<a href='/led_all/off'>Turn OFF_ALL</a>";
  html += "</html>";

  return html;
}

void setup()
{
  Serial.begin(9600);
  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(LED_PIN_3, OUTPUT);
  pinMode(LED_PIN_4, OUTPUT);
  digitalWrite(LED_PIN_1, LED_state);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print the ESP32's IP address
  Serial.print("ESP32 Web Server's IP address: ");
  Serial.println(WiFi.localIP());

  // home page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /");
    request->send(200, "text/html", getHTML()); });

  // Route to control the LED
  server.on("/led1/on", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led1/on");
    LED_state = HIGH;
    digitalWrite(LED_PIN_1, LED_state);
    request->send(200, "text/html", getHTML()); });
  server.on("/led1/off", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led1/off");
    LED_state = LOW;
    digitalWrite(LED_PIN_1, LED_state);
    request->send(200, "text/html", getHTML()); });

  // LED2
  server.on("/led2/on", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led2/on");
    LED_state = HIGH;
    digitalWrite(LED_PIN_2, LED_state);
    request->send(200, "text/html", getHTML()); });
  server.on("/led2/off", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led2/off");
    LED_state = LOW;
    digitalWrite(LED_PIN_2, LED_state);
    request->send(200, "text/html", getHTML()); });

  // LED3
  server.on("/led3/on", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led3/on");
    LED_state = HIGH;
    digitalWrite(LED_PIN_3, LED_state);
    request->send(200, "text/html", getHTML()); });
  server.on("/led3/off", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led3/off");
    LED_state = LOW;
    digitalWrite(LED_PIN_3, LED_state);
    request->send(200, "text/html", getHTML()); });

  // LED4
  server.on("/led4/on", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led4/on");
    LED_state = HIGH;
    digitalWrite(LED_PIN_4, LED_state);
    request->send(200, "text/html", getHTML()); });
  server.on("/led4/off", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led4/off");
    LED_state = LOW;
    digitalWrite(LED_PIN_4, LED_state);
    request->send(200, "text/html", getHTML()); });

  // ALL LED
  server.on("/led_all/on", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led_all/on");
    LED_state = HIGH;
    digitalWrite(LED_PIN_1, LED_state);
    digitalWrite(LED_PIN_2, LED_state);
    digitalWrite(LED_PIN_3, LED_state);
    digitalWrite(LED_PIN_4, LED_state);
    request->send(200, "text/html", getHTML()); });
  server.on("/led_all/off", HTTP_GET, [](AsyncWebServerRequest *request)
            {
    Serial.println("ESP32 Web Server: New request received:");
    Serial.println("GET /led_all/off");
    LED_state = LOW;
    digitalWrite(LED_PIN_1, LED_state);
    digitalWrite(LED_PIN_2, LED_state);
    digitalWrite(LED_PIN_3, LED_state);
    digitalWrite(LED_PIN_4, LED_state);
    request->send(200, "text/html", getHTML()); });

  // Start the server
  server.begin();
}

void loop()
{
  // Your code here
}
