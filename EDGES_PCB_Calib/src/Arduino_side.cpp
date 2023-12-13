// Include necessary libraries
#include <Arduino.h>

// Define LED pin
const int ledPin = 32;
const int conect = 34;

void setup() {
  // Start serial communication
  Serial.begin(9600);



  // Initialize LED pin as an output
  pinMode(ledPin, OUTPUT);
  pinMode(conect, OUTPUT);

  while (!Serial) {
    // Wait for the serial port to be opened
     digitalWrite(conect, HIGH);
     delay(1000);
     digitalWrite(conect, LOW);
     delay(1000);
     //Serial.println("No Command received: ");
  }

  // Print a message to indicate that the Serial Monitor is active
  Serial.println("Serial Monitor link is active!");

}

void loop() {
  // Check if data is available to read from serial port
  if (Serial.available() > 0) {
    // Read the incoming command
    String command = Serial.readStringUntil('\n');
    x = command.split("x")
    serial.println(x[1]);
    // Process the command
    if (command == "ON") {
      digitalWrite(ledPin, HIGH);  // Turn the LED on
      Serial.println("LED is ON");
    } else if (command == "OFF") {
      digitalWrite(ledPin, LOW);  // Turn the LED off
      Serial.println("LED is OFF");
    } else {
      Serial.println("Invalid command");
    }
    } 
    
  // Add a short delay for stability
  delay(1000);
}