
 
#define trigPin 12
#define echoPin 13
#define ledPin 8
#define servoPin 6
#include <Servo.h>

Servo servo;
int servoangle = 90;
unsigned long actualTime = 0;
unsigned long lastTime = 0;
unsigned long lastTimeBlinker = 0;
unsigned long timeDiff = 0;
boolean leftBlinkers = false;
int length = 30;
char buffer [31];
boolean haveNewData = false;
String dataToSend;    
int leftBlinkersTurnedOn = 0;


void setup() {
  Serial.begin (9600);
  delay(500);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  servo.attach(servoPin);
  servo.write(servoangle);
}
 
void loop() {  
  actualTime = millis();
  recvWithStartEndMarkers();
  measureDistance();
  sendDataSerial();
  ledBlinker();
  servoSteering();
} 

void ledBlinker(){
   if(leftBlinkersTurnedOn){
     if(actualTime - lastTimeBlinker>=300UL){
        if(leftBlinkers == false){
          leftBlinkers = true;
          digitalWrite(ledPin, HIGH);
        }else{
          leftBlinkers = false;
          digitalWrite(ledPin, LOW);
        } 
        lastTimeBlinker = actualTime; 
      }
    }else{
      digitalWrite(ledPin, LOW);
    }
}

void servoSteering(){
  servo.write(servoangle);
}

void sendDataSerial(){
  if (dataToSend != ""){
    Serial.println("<" + dataToSend + ">");
    Serial.flush();
    dataToSend = "";
  }
}
 
void measureDistance() {
  if((actualTime - lastTime)>=800UL){
    long timeOfTravel, distance;
   
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
   
    timeOfTravel = pulseIn(echoPin, HIGH);
    distance = timeOfTravel / 58;
    dataToSend = dataToSend + distance;
    lastTime = actualTime; 
  }
}

void recvWithStartEndMarkers()
{
     static boolean recvInProgress = false;
     static byte ndx = 0;
     char startMarker = '[';
     char endMarker = ']';
     char rc;
 
     if (Serial.available() > 0) 
     {
          rc = Serial.read();
          if (recvInProgress == true) 
          {
               if (rc != endMarker) 
               {
                    buffer[ndx] = rc;
                    ndx++;
                    if (ndx > length) { ndx = length; }
               }
               else 
               {
                     buffer[ndx] = '\0'; // terminate the string
                     recvInProgress = false;
                     ndx = 0;
                     haveNewData = true;
                     splitRecvData();
               }
          }
          else if (rc == startMarker) { recvInProgress = true; }
     }
}

void splitRecvData(){
  char * strtokIndx;
  strtokIndx = strtok(buffer, ",");
  leftBlinkersTurnedOn = atoi(strtokIndx);
  strtokIndx = strtok(NULL, ",");
  servoangle = atoi(strtokIndx);
}
