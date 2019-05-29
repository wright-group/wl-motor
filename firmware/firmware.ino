#include <RotaryEncoder.h>
RotaryEncoder encoder(A2, A3);
const int stepPin = 5;
const int dirPin = 4;
int homePin = A6; 

int newPos; //say which direction the translation stage should move 
int steps = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  pinMode(homePin, INPUT_PULLUP);

  Serial.begin(57600);
  Serial.println("Current position");

  PCICR |= (1 << PCIE1);
  PCMSK1 |= (1 << PCINT10) | (1 << PCINT11);


}

ISR(PCINT1_vect) {
  encoder.tick(); // just call tick() to check the state.
}

void loop() {
  static int pos = 0;

  int newPos = encoder.getPosition();
  if (pos < newPos) {
    digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
    // Makes 200 pulses for making one full cycle rotation
      for(int x = 0; x < 80; x++) {
        rotate_CCW();
      }
    Serial.print(newPos);
    Serial.println();
    pos = newPos;
  }
  else if (pos > newPos) {
    digitalWrite(dirPin, LOW);
    for(int x = 0; x < 80; x++) {
      rotate_CW();
    }
    Serial.print(newPos);
    Serial.println();
    pos = newPos;
  }
if (Serial.available() > 0) {
    newPos = Serial.parseInt(); 
  }
  if (newPos > pos) {
    steps = newPos - pos;
    for (int x=0; x < steps; x++) { 
      rotate_CW();
    }
   pos = newPos;
   encoder.setPosition(pos);
   Serial.println(pos);
  }
  else if (newPos < pos) {
    steps = pos - newPos;
    for (int x=0; x < steps; x++){
      rotate_CCW();
    }
    pos = newPos;
    encoder.setPosition(pos);
    Serial.println(pos);
  }

}


void rotate_CW(){
  digitalWrite(dirPin,HIGH);
    digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
}

void rotate_CCW (){
  if (digitalRead(homePin) {
   digitalWrite (dirPin, LOW);
    digitalWrite(stepPin, HIGH);
      delayMicroseconds(500);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(500);
  }
  else {
    pos = 0;
  }
}
