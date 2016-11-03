import os;
import sys;
import time
import serial

ser = serial.Serial(

	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)



file=open('test.txt');

for line in iter(file) :
	print line;
        for ch in line :
                 ser.write(ch);
file.close;
