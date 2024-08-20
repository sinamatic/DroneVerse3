// change this to platformio project or use arduino ide
#include <Arduino.h>

long duration;
int distance;

const int trigPin = 4;
const int echoPin = 5;
const int minDistance = 5;  // Minimale Distanz in cm, bei der der Timer gestartet werden soll
const int maxDistance = 45; // Maximale Distanz in cm, bei der der Timer gestoppt werden soll

unsigned long startTime;
unsigned long stopTime; // Variable zum Speichern der Zeit, wenn der Timer gestoppt wird
bool timerRunning = false;
bool measurementStarted = false; // Flag, ob die Messung gestartet wurde
bool initialWaitDone = false;    // Flag, um die initiale Wartezeit zu steuern
unsigned long waitStartTime;

void setup()
{
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(115200);
}

void loop()
{
  if (Serial.available() > 0)
  {
    char input = Serial.read();
    if (input == 's' && !measurementStarted)
    {
      measurementStarted = true;
      initialWaitDone = false; // Reset initial wait
    }
    if (input == 'p' && timerRunning)
    {
      stopTimer();
      measurementStarted = false;
    }
  }

  if (measurementStarted && !timerRunning)
  {
    // Abstand messen
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;

    if (distance >= minDistance && distance <= maxDistance)
    {
      startTimer();
      waitStartTime = millis(); // Start the wait time
    }
  }

  if (timerRunning)
  {
    // Zeit messen und anzeigen
    printElapsedTime();

    // Initiale 10 Sekunden Wartezeit
    if (!initialWaitDone && millis() - waitStartTime >= 20000)
    {
      initialWaitDone = true;
    }

    // Abstand messen nur nach der initialen Wartezeit
    if (initialWaitDone)
    {
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

      duration = pulseIn(echoPin, HIGH);
      distance = duration * 0.034 / 2;

      if (distance >= minDistance && distance <= maxDistance)
      {
        stopTimer();
        measurementStarted = false; // Ermöglicht eine neue Messung nach dem Stopp
      }
    }
  }

  delay(100); // Kurze Pause, um die Seriellenausgabe lesbar zu machen
}

void startTimer()
{
  startTime = millis();
  timerRunning = true;
}

void stopTimer()
{
  stopTime = millis(); // Speichern der Zeit bei Timer-Stopp
  timerRunning = false;
  printElapsedTime(); // Zeit seit dem Timer-Start anzeigen
}

void printElapsedTime()
{
  unsigned long currentTime = timerRunning ? millis() : stopTime;
  unsigned long elapsedTime = currentTime - startTime;

  unsigned long minutes = (elapsedTime / 60000) % 60;
  unsigned long seconds = (elapsedTime / 1000) % 60;
  unsigned long milliseconds = elapsedTime % 1000;

  Serial.print(minutes);
  Serial.print(":");
  Serial.print(seconds);
  Serial.print(".");
  Serial.println(milliseconds);
}