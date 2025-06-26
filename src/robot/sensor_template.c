/*
  HC-SR04 Ultrasonic Sensor Test for ESP32 WROOM 32
  
  Connections:
  HC-SR04 VCC to ESP32 VCC/VIN (Use 5V for original HC-SR04, 3.3V for HC-SR04+)
  HC-SR04 GND to ESP32 GND
  HC-SR04 TRIG to ESP32 GPIO 12
  HC-SR04 ECHO to ESP32 GPIO 23
*/

// Define pins
const int trigPin = 12;
const int echoPin = 23;

// Define constants
#define SOUND_SPEED 0.034  // Speed of sound in cm/uS
#define CM_TO_INCH 0.393701  // Conversion factor from cm to inches

// Variables
long duration;
float distanceCm = 0;
float distanceInch = 0;
int errorCount = 0;
unsigned long lastReadingTime = 0;
bool sensorConnected = false;

void setup() {
  // Initialize Serial
  Serial.begin(115200);
  
  // Set pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initial state for trigger pin
  digitalWrite(trigPin, LOW);
  
  delay(1000);  // Wait for serial to connect

  Serial.println("\nHC-SR04 Ultrasonic Sensor Test");
  Serial.println("TRIG Pin: 12, ECHO Pin: 23");
}

void loop() {
  // Measure distance using median filtering
  float distance = getMedianDistance(5);  // Take 5 readings and use median
  
  // Process reading
  if (distance > 0) {
    // Valid reading
    if (!sensorConnected) {
      Serial.println("Sensor connected and working!");
      sensorConnected = true;
    }
    
    errorCount = 0;
    lastReadingTime = millis();
    
    // Convert and display
    distanceCm = distance;
    distanceInch = distanceCm * CM_TO_INCH;
    
    Serial.print("Distance: ");
    Serial.print(distanceCm, 1);
    Serial.print(" cm (");
    Serial.print(distanceInch, 1);
    Serial.println(" inches)");
  } else {
    // Invalid reading
    errorCount++;
    
    // Only show error message occasionally
    if (errorCount == 5 || errorCount % 20 == 0) {
      Serial.println("\nWarning: No valid distance readings");
      Serial.println("Possible issues:");
      Serial.println("1. Check connections: TRIG->GPIO12, ECHO->GPIO23");
      Serial.println("2. Check power: HC-SR04 needs 5V, HC-SR04+ can use 3.3V");
      Serial.println("3. Ensure object is within range (2-400cm)");
    }
    
    if (millis() - lastReadingTime > 10000 && sensorConnected) {
      Serial.println("Sensor connection lost. Please check hardware!");
      sensorConnected = false;
    }
  }
  
  // Delay between measurements
  delay(300);
}

float getMedianDistance(int samples) {
  float measurements[samples];
  int validCount = 0;
  
  // Take multiple readings
  for (int i = 0; i < samples; i++) {
    float measure = takeSingleMeasurement();
    if (measure > 0) {
      measurements[validCount++] = measure;
    }
    delay(20);  // Brief delay between readings
  }
  
  // If no valid readings, return error
  if (validCount == 0) {
    return -1;
  }
  
  // Sort measurements (bubble sort)
  for (int i = 0; i < validCount - 1; i++) {
    for (int j = 0; j < validCount - i - 1; j++) {
      if (measurements[j] > measurements[j + 1]) {
        // Swap
        float temp = measurements[j];
        measurements[j] = measurements[j + 1];
        measurements[j + 1] = temp;
      }
    }
  }
  
  // Return median value
  return measurements[validCount/2];
}

float takeSingleMeasurement() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Generate a 10µs pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Measure the duration of the echo pulse with appropriate timeout
  // Using a longer timeout helps prevent zero readings
  duration = pulseIn(echoPin, HIGH, 30000);
  
  // Check if we got a pulse
  if (duration == 0) {
    return -1;  // No echo received within timeout
  }
  
  // Calculate distance from duration
  float distance = duration * SOUND_SPEED / 2;
  
  // Check if distance is within valid range
  if (distance < 2 || distance > 400) {
    return -1;  // Out of range
  }
  
  return distance;
}
