int trig1 = 2;
int echo1 = 3;
int trig2 = 4;
int echo2 = 5;
int trig3 = 6;
int echo3 = 7;


void setup() {
 Serial.begin(9600); // set the baud rate
 Serial.println("Ready"); // print "Ready" once

 pinMode(trig1, OUTPUT);
 pinMode(echo1, INPUT);
 pinMode(trig2, OUTPUT);
 pinMode(echo2, INPUT);
 pinMode(trig3, OUTPUT);
 pinMode(echo3, INPUT);
}


void loop() {

 /* The following trigPin/echoPin cycle is used to determine the
 distance of the nearest object by bouncing soundwaves off of it. */
 digitalWrite(trig1, LOW);
 delayMicroseconds(2);
 digitalWrite(trig1, HIGH);
 delayMicroseconds(10);
 digitalWrite(trig1, LOW);
 long dur1 = pulseIn(echo1, HIGH);

 digitalWrite(trig2, LOW);
 delayMicroseconds(2);
 digitalWrite(trig2, HIGH);
 delayMicroseconds(10);
 digitalWrite(trig2, LOW);
 long dur2 = pulseIn(echo2, HIGH);

 digitalWrite(trig3, LOW);
 delayMicroseconds(2);
 digitalWrite(trig3, HIGH);
 delayMicroseconds(10);
 digitalWrite(trig3, LOW);
 long dur3 = pulseIn(echo3, HIGH);

 //Calculate the distance (in cm) based on the speed of sound.
 long dist1 = dur1/59;
 long dist2 = dur2/59;
 long dist3 = dur3/59;

Serial.print(dist1);
Serial.print("|");
Serial.print(dist2);
Serial.print("|");
Serial.print(dist3);
Serial.println();

delay(500); // delay for 1/10 of a second
}
