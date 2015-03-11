#!/usr/bin/python

# Waldo Playback - Sends data from a Waldo file to the CHIA through Serial
# 
#     This program works in association with the Arduino
#     sketch: mon2_chia_new_Vn
#
#    
#
#     Usage: waldo_playback.py <filename> <port>
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

if not os.path.isfile(sys.argv[1]):
	print sys.argv[1] + " does not exist.",
	sys.exit(2)
else:
	response = raw_input("Begin playback? [Y|n]: ")
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
f = open(sys.argv[1], 'r')

# Set the Arduino to Playback Mode by sending control string
inputSerial.write("+++PLAYBACK+++")
inputSerial.write("\n")
inputSerial.flush()
time.sleep(1)
while inputSerial.inWaiting() != 0:
	data = inputSerial.readline()
	print data

# Playback data from Arduino until the file is fully read
for line in f:
	start_time = time.time()
	if inputSerial.inWaiting() != 0:
		data = inputSerial.readline()
		print data
		if data[0] == "-":
			print("Safety switch is off. Playback suspended.")
			while True: 
				data = inputSerial.readline()
				if data[0] == "+":
					break
				else:
					print data
					time.sleep(0.01)
			print("Safety switch is on. Playback resumed.")
			start_time = time.time()
	if interrupted == True:
		print("Interrupted. Exiting playback.")
		inputSerial.write("+++STOP+++")
		inputSerial.write("\n")
		sys.exit()
	if line[0] == "1" or line[0] == "2":
		inputSerial.write(line)
	while time.time()-start_time < 0.1:
		pass

# Set the Arduino to Stop Mode
inputSerial.write("+++STOP+++")
inputSerial.write("\n")

print("Playback finished. CHIAS returned to Stopped.")

# Close the output file
f.close()
