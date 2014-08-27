int trigger = 2;
int echo = 3;


void setup() {
 Serial.begin(9600); // set the baud rate
 Serial.println("Ready"); // print "Ready" once

 pinMode(trigger, OUTPUT);
 pinMode(echo, INPUT);

 }


void loop() {

 /* The following trigPin/echoPin cycle is used to determine the
 distance of the nearest object by bouncing soundwaves off of it. */
 digitalWrite(trigger, LOW);
 delayMicroseconds(2);

 digitalWrite(trigger, HIGH);
 delayMicroseconds(10);

 digitalWrite(trigger, LOW);
 long duration = pulseIn(echo, HIGH);

 //Calculate the distance (in cm) based on the speed of sound.
 long distance = duration/59;

Serial.println(distance); // send the data back in a new line so that it is not all one long line


delay(100); // delay for 1/10 of a second
}
