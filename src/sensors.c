// Define the Arduino pins connected to the DF-MD V1.3 shield for Motor 1
#define MOTOR1_PWM_PIN 10  // E1 - Speed Control (PWM)
#define MOTOR1_DIR_PIN 12  // M1 - Direction Control


// --- Motor Control Functions ---


// Function to drive the motor forward
// speed: 0 (stopped) to 255 (full speed)
void motorForward(int speed) {
  // Set Direction Pin HIGH for forward (swap HIGH/LOW if motor spins wrong way)
  digitalWrite(MOTOR1_DIR_PIN, HIGH);
  analogWrite(MOTOR1_PWM_PIN, speed); // Set speed using PWM
}


// Function to drive the motor backward
// speed: 0 (stopped) to 255 (full speed)
void motorBackward(int speed) {
  // Set Direction Pin LOW for backward (swap HIGH/LOW if motor spins wrong way)
  digitalWrite(MOTOR1_DIR_PIN, LOW);
  analogWrite(MOTOR1_PWM_PIN, speed); // Set speed using PWM
}


// Function to stop the motor
void motorStop() {
  digitalWrite(MOTOR1_DIR_PIN, LOW);  // Set direction pin to a known state (optional)
  analogWrite(MOTOR1_PWM_PIN, 0);     // Set speed PWM to 0 (effectively stops power)
}


// --- Arduino Setup ---
void setup() {
  // Initialize Serial communication for debugging output
  Serial.begin(9600);
  Serial.println("DF-MD V1.3 - Motor 1 - 10 Second Run Test");


  // Set the motor control pins as outputs
  pinMode(MOTOR1_PWM_PIN, OUTPUT);
  pinMode(MOTOR1_DIR_PIN, OUTPUT);


  // Ensure motor is stopped at the beginning
  Serial.println("Initializing motor stopped...");
  motorStop();
  delay(1000); // Wait 1 second before starting
}


// --- Arduino Loop ---
void loop() {
  // 1. Start Motor Forward
  int runSpeed = 255; // Set desired speed (0-255)
  Serial.print("Running motor FORWARD at speed ");
  Serial.print(runSpeed);
  Serial.println(" for 10 seconds...");
  motorForward(runSpeed); // Start the motor forward


  // 2. Wait for 10 seconds
  // delay() takes milliseconds, so 10 seconds = 10 * 1000 = 10000 ms
  delay(10000);


  // 3. Stop Motor
  Serial.println("Stopping motor.");
  motorStop();


  // 4. Pause before repeating
  Serial.println("Cycle complete. Pausing for 3 seconds...");
  delay(3000); // Wait for 3 seconds before the loop starts again
}