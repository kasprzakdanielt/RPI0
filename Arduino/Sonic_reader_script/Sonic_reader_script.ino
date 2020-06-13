
 
#define trigPin 12
#define echoPin 13
#define ledPin 8
unsigned long actualTime = 0;
unsigned long lastTime = 0;
unsigned long timeDiff = 0;
int length = 30;
char buffer [31];
boolean haveNewData = false;
String dataToSend;    
    boolean ledstatus = false;
void setup() {
  Serial.begin (9600);
  delay(500);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
}
 
void loop() {  
  
      actualTime = millis();
      timeDiff = actualTime - lastTime;
      recvWithStartEndMarkers();
      if(timeDiff>=800UL){
  measureDistance();
      }
  if(ledstatus){
    digitalWrite(ledPin, HIGH);
  }else if (!ledstatus){
    digitalWrite(ledPin, LOW);
  }
  sendDataSerial();
   if(buffer[0]=='a'){
      ledstatus = true;
     } else if(buffer[0]=='b'){
      ledstatus = false;
     }
} 

void sendDataSerial(){
  if (dataToSend != ""){
  Serial.println("<" + dataToSend + ">");
  Serial.flush();
  dataToSend = "";
  }
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
  lastTime = actualTime; 
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
               }
          }
          else if (rc == startMarker) { recvInProgress = true; }
     }
}
