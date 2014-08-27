from time import sleep
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600) # Establish the connection on a specific port
while True:
     print ser.readline() # Read the newest output from the Arduino
     sleep(.1) # Delay for one tenth of a second
