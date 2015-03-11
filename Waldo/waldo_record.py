#!/usr/bin/python

# Waldo Record - collect data from Waldo arduino and save to file
# 
#     This program works in association with the Arduino
#     sketch: mon2_chia_new_Vn
#
#     Records remote control data send by Arduino and writes to 
#     the designated file. This file can later be used to play
#     back control data with waldo_playback.py
#
#     Usage: waldo_record.py <filename> <port>
#
import serial
import signal
import time
import sys
import os.path

# Check that filename and port are specified
if len(sys.argv) < 3:
	print "Please specify a filename or port"
	sys.exit(2)

if os.path.isfile(sys.argv[1]):
	print sys.argv[1] + " already exists. ",
	response = raw_input("Overwrite? [Y|n]: ")
	if response != 'Y':
		sys.exit(2)

			     
# Interrupt flag - will set to True to terminate program
global interrupted
interrupted = False

# Handler for sigint
def signal_handler(signum, frame):
	interrupted = True

# Attach the handler
signal.signal(signal.SIGINT, signal_handler)

# Start the serial port (causes the Arduido to reset so wait a few
# seconds for that to happen
# Linux port: '/dev/tty.usbmodemfd111'
inputSerial = serial.Serial(sys.argv[2], 9600)
time.sleep(5)

# Read serial data sent by the Arduino to enable sending
while inputSerial.inWaiting() != 0:
	data = inputSerial.readline()
	print data

# Open the outputfile
f = open(sys.argv[1], 'w')

# Set the Arduino to Record Mode by sending control straing
inputSerial.write("+++RECORD+++")
inputSerial.write("\n")
inputSerial.flush()

# Record data from Arduino until program is terminated
while interrupted == False:
	if inputSerial.inWaiting != 0:
		data = inputSerial.readline()
		f.write(data)
		print (data)
		time.sleep(0.01)

# Set the Arduino to Stop Mode
inputSerial.write("+++STOP+++")
inputSerial.write("\n")

# Close the output file
f.close()
