#include <RotaryEncoder.h>
#define ENCODER_NUM_STEPS 20
#define BUFFSIZE 100

RotaryEncoder encoder(A2, A3);
const int stepPin = 5;
const int dirPin = 4;
const int homePin = A6;

long destination; //say which direction the translation stage should move
long pos;
long encoder_position;

void setup() {
  pos = 0;

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  pinMode(homePin, INPUT_PULLUP);

  Serial.begin(57600);
}

void serialEvent() {
  char buf[BUFFSIZE];
  int numRead = Serial.readBytesUntil('\n', buf, BUFFSIZE);
  buf[numRead] = 0;
  destination = atol(buf);
  if (pos == destination) {
    printPos();
  }
  Serial.flush();
}

void loop() {
  encoder.tick();
  encoder_position = encoder.getPosition();
  if (encoder_position) {
    destination -= encoder_position * ENCODER_NUM_STEPS;
    encoder.setPosition(0);
  }

  if (destination != pos) {
    rotate(destination > pos);
  }
}
void rotate(int direction) {
  // TODO: read home pin, prevent moving in negative direction
  digitalWrite(dirPin, direction);
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(100);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(200);
  pos += 2 * direction - 1;
  if (pos == destination) {
    printPos();
  }
}
void printPos() {
  Serial.print("S");
  Serial.print(pos);
  Serial.println("E");
}
