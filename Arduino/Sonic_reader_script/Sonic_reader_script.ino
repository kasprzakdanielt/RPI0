
 
#define trigPin 12
#define echoPin 13
#define ledPin 8

const byte maxDataLength = 30;  // maxDataLength is the maximum length allowed for received data.
char receivedChars[31] ;    
String dataToSend;    
     char startMarker = '[';
     char endMarker = ']';
     boolean recvInProgress = false;
    boolean ledstatus = false;
void setup() {
  Serial.begin (115200);
  delay(500);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
}
 
void loop() {  
  if (Serial.available() > 0) {
  if (Serial.read() == startMarker){
      recvInProgress == true;
      recvWithStartEndMarkers();
  }}
  measureDistance();
  if(ledstatus){
    digitalWrite(ledPin, HIGH);
  }else if (!ledstatus){
    digitalWrite(ledPin, LOW);
  }
  sendDataSerial();
} 

void sendDataSerial(){
  Serial.println("<" + dataToSend + ">");
  Serial.flush();
  dataToSend = "";
}
 
void measureDistance() {
  long timeOfTravel, distance;
 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
 
  timeOfTravel = pulseIn(echoPin, HIGH);
  distance = timeOfTravel / 58;
 
  dataToSend = dataToSend + distance;
}

void recvWithStartEndMarkers()
{
     static boolean recvInProgress = false;
     static byte ndx = 0;

     char rc;
          rc = Serial.read();
          if (recvInProgress == true) 
          {
               if (rc != endMarker) 
               {
                    receivedChars[ndx] = rc;
                    ndx++;
                    if (ndx > maxDataLength) { ndx = maxDataLength; }
               }
               else 
               {
                     receivedChars[ndx] = '\0'; // terminate the string
                     recvInProgress = false;
                     ndx = 0;
               }
          }
     if(receivedChars[0]=='a'){
      ledstatus = true;
     } else{
      ledstatus = false;
     }
}
