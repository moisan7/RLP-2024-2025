// --- ESP32 Pin Assignments for DF-MD v1.4 Shield ---
// Motor 1
#define MOTOR1_PWM_PIN 25   // Must be PWM-capable (e.g., GPIO 25)
#define MOTOR1_DIR_PIN 26   
// Motor 2
#define MOTOR2_PWM_PIN 27   // Must be PWM-capable (e.g., GPIO 27)
#define MOTOR2_DIR_PIN 14   

// ======================== MOTOR 1 FUNCTIONS ========================
void motor1Forward(int speed) {
  digitalWrite(MOTOR1_DIR_PIN, HIGH);
  analogWrite(MOTOR1_PWM_PIN, speed);
}

void motor1Backward(int speed) {
  digitalWrite(MOTOR1_DIR_PIN, LOW);
  analogWrite(MOTOR1_PWM_PIN, speed);
}

void motor1Stop() {
  analogWrite(MOTOR1_PWM_PIN, 0);
}

// ======================== MOTOR 2 FUNCTIONS ========================
void motor2Forward(int speed) {
  digitalWrite(MOTOR2_DIR_PIN, HIGH);
  analogWrite(MOTOR2_PWM_PIN, speed);
}

void motor2Backward(int speed) {
  digitalWrite(MOTOR2_DIR_PIN, LOW);
  analogWrite(MOTOR2_PWM_PIN, speed);
}

void motor2Stop() {
  analogWrite(MOTOR2_PWM_PIN, 0);
}

// ======================== SETUP ========================
void setup() {
  Serial.begin(115200);
  Serial.println("DF-MD v1.4 - Dual Motor Control");

  // Initialize motor control pins
  pinMode(MOTOR1_DIR_PIN, OUTPUT);
  pinMode(MOTOR1_PWM_PIN, OUTPUT);
  pinMode(MOTOR2_DIR_PIN, OUTPUT);
  pinMode(MOTOR2_PWM_PIN, OUTPUT);

  // Start with motors stopped
  motor1Stop();
  motor2Stop();
  delay(1000);
}

// ======================== MAIN LOOP ========================
void loop() {
  Serial.println("Both motors FORWARD at 75% speed");
  motor1Forward(191);  // 75% of 255 ≈ 191
  motor2Forward(191);
  delay(5000);

  Serial.println("Both motors BACKWARD at full speed");
  motor1Backward(255);
  motor2Backward(255);
  delay(5000);

  Serial.println("Stopping both motors");
  motor1Stop();
  motor2Stop();
  delay(3000);
}