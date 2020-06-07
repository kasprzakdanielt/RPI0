
 
#define trigPin 12
#define echoPin 13
 
void setup() {
  Serial.begin (9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}
 
void loop() {  
  Serial.println("Distance: " + String(measureDistance()));
} 
 
int measureDistance() {
  long timeOfTravel, distance;
 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  timeOfTravel = pulseIn(echoPin, HIGH);
  distance = timeOfTravel / 58;
 
  return distance;
}
