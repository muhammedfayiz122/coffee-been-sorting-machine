#include <Stepper.h>
#include <Servo.h>

//-------------------------------------------------------------------
// System State Management
//-------------------------------------------------------------------
enum SystemState {
  WAITING_FOR_START,
  RUNNING,
  STOPPED
};

SystemState systemState = WAITING_FOR_START;

//-------------------------------------------------------------------
// Command Constants (must match Python commands)
//-------------------------------------------------------------------
const String CMD_START  = "START";
const String CMD_STOP   = "STOP";
const String CMD_STEP   = "STEP";
const String CMD_MEDIUM = "1";
const String CMD_LOW    = "0";
const String CMD_DARK   = "2";

//-------------------------------------------------------------------
// Hardware Configuration
//-------------------------------------------------------------------
// Stepper Motor (28BYJ-48) configuration:
// It requires ~2048 half-steps per revolution.
// Wiring order for the ULN2003 driver: IN1, IN3, IN2, IN4 (pins 2, 3, 4, 5)
const int stepsPerRevolution = 2048;
Stepper stepper(stepsPerRevolution, 2, 3, 4, 5);

// Motor driver pins (optional disabling outputs)
const int motorPins[] = {2, 3, 4, 5};
const int numMotorPins = sizeof(motorPins) / sizeof(motorPins[0]);

// Servo Motor Configuration
Servo sorterServo;
const int servoPin = 6;
// Servo angles for sorting (adjust these values as needed)
const int MEDIUM_ANGLE = 90;  // Default position for medium-colored coffee
const int LOW_ANGLE    = 55;  // Position for low-colored coffee
const int DARK_ANGLE   = 128; // Position for dark-colored coffee

//-------------------------------------------------------------------
// Heartbeat Timeout for READY signal
//-------------------------------------------------------------------
unsigned long lastReadyTime = 0;
const unsigned long READY_INTERVAL = 3000; // milliseconds

//-------------------------------------------------------------------
// Helper Functions
//-------------------------------------------------------------------

/**
* @brief Disables the motor driver outputs to reduce heating.
*/
void disableMotorDriver() {
  for (int i = 0; i < numMotorPins; i++) {
    digitalWrite(motorPins[i], LOW);
  }
}

/**
* @brief Processes an incoming command string.
* 
* @param cmd The command received via Serial.
*/
void processCommand(const String &cmd) {
  if (cmd == CMD_STOP) {
    Serial.println("Stopping process...");
    disableMotorDriver();
    systemState = STOPPED;
  }
  else if (cmd == CMD_LOW) {
    sorterServo.write(LOW_ANGLE);
    Serial.println("Servo set to LOW position.");
  }
  else if (cmd == CMD_MEDIUM) {
    sorterServo.write(MEDIUM_ANGLE);
    Serial.println("Servo set to MEDIUM position.");
  }
  else if (cmd == CMD_DARK) {
    sorterServo.write(DARK_ANGLE);
    Serial.println("Servo set to DARK position.");
  }
  else if (cmd == CMD_STEP) {
    Serial.println("Rotating stepper motor 60° clockwise...");
    stepper.step(stepsPerRevolution / 6);
    Serial.println("READY");
  }
  else if (cmd == "+") {
    stepper.step(stepsPerRevolution / 18);
  }
  else if (cmd == "-") {
    stepper.step(-1 * stepsPerRevolution / 18);
  }
  else if (cmd ==)
  else {
    Serial.print("Unrecognized command: ");
    Serial.println(cmd);
  }
}

//-------------------------------------------------------------------
// Setup
//-------------------------------------------------------------------
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for Serial port connection (if needed)
  }
  
  // Configure stepper motor speed (20 RPM)
  stepper.setSpeed(17);
  
  // Attach servo and initialize to default position
  sorterServo.attach(servoPin);
  sorterServo.write(MEDIUM_ANGLE);
  Serial.println("Servo to neutral postion");
  
  // Configure motor pins as outputs
  for (int i = 0; i < numMotorPins; i++) {
    pinMode(motorPins[i], OUTPUT);
  }
  
  // Wait for the "START" command from the Python script
  Serial.println("Waiting for 'START' signal...");ZZZZZZZZ
  while (systemState == WAITING_FOR_START) {
    // Serial.println(systemState);
    Serial.println("Waiting for 'START' signal...");
    if (Serial.available() > 0) {
      String input = Serial.readStringUntil('\n');
      input.trim(); // Remove extraneous whitespace
      if (input == CMD_START) {
        systemState = RUNNING;
        Serial.println("START command received. System is now running.");
        // Signal readiness for the first cycle.
        Serial.println("READY");
        lastReadyTime = millis();
      }
      else if (input == CMD_STOP) {
        Serial.println("STOP command received during startup. Halting.");
        disableMotorDriver();
        systemState = STOPPED;
      }
    }
  }
}

//-------------------------------------------------------------------
// Main Loop
//-------------------------------------------------------------------
void loop() {
  
  // Process incoming serial commands if available.
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  // Clean up the command string
    processCommand(command);
  }
  Serial.println("READY");
  
  // Minimal delay to yield processor time
}
