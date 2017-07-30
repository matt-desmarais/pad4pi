#!/usr/bin/python

from pad4pi import rpi_gpio
import time
import sys
import RPi.GPIO as GPIO
import sys
import os
from squid import *
import re
import subprocess

usbDisarm = 0
Relay_Pin = 10

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

rgb = Squid(16, 20, 21)

#if usbDisarm == 0:
#    rgb.set_color(BLUE)
#else:
rgb.set_color(GREEN)


global counter
counter = 1
passcode = ""
entered_passcode = ""
correct_passcode = "1234"
timer = ""

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_4_by_3_keypad()

#def enterCode():
#    keypad.registerKeyPressHandler(key_pressed2)

def cleanup():
    global keypad
    keypad.cleanup()

global Buzzer_Pin
Buzzer_Pin = 23


def play(melody,tempo,pause,pace=0.800):
	
	for i in range(0, len(melody)):		# Play song
		
		noteDuration = pace/tempo[i]
		buzz(melody[i],noteDuration)	# Change the frequency along the song note
		
		pauseBetweenNotes = noteDuration * pause
		time.sleep(pauseBetweenNotes)


def buzz(frequency, length):	 #create the function "buzz" and feed it the pitch and duration)
	global Buzzer_Pin
	if(frequency==0):
		time.sleep(length)
		return
	period = 1.0 / frequency 		 #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
	delayValue = period / 2		 #calcuate the time for half of the wave
	numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
	for i in range(numCycles):		#start a loop from 0 to the variable "cycles" calculated above
	    GPIO.output(Buzzer_Pin, True)	 #set pin 27 to high
	    time.sleep(delayValue)		#wait with pin 27 high
	    GPIO.output(Buzzer_Pin, False)		#set pin 27 to low
	    time.sleep(delayValue)		#wait with pin 27 low


notes = {
	'B0' : 31,
	'C1' : 33, 'CS1' : 35,
	'D1' : 37, 'DS1' : 39,
	'EB1' : 39,
	'E1' : 41,
	'F1' : 44, 'FS1' : 46,
	'G1' : 49, 'GS1' : 52,
	'A1' : 55, 'AS1' : 58,
	'BB1' : 58,
	'B1' : 62,
	'C2' : 65, 'CS2' : 69,
	'D2' : 73, 'DS2' : 78,
	'EB2' : 78,
	'E2' : 82,
	'F2' : 87, 'FS2' : 93,
	'G2' : 98, 'GS2' : 104,
	'A2' : 110, 'AS2' : 117,
	'BB2' : 123,
	'B2' : 123,
	'C3' : 131, 'CS3' : 139,
	'D3' : 147, 'DS3' : 156,
	'EB3' : 156,
	'E3' : 165,
	'F3' : 175, 'FS3' : 185,
	'G3' : 196, 'GS3' : 208,
	'A3' : 220, 'AS3' : 233,
	'BB3' : 233,
	'B3' : 247,
	'C4' : 262, 'CS4' : 277,
	'D4' : 294, 'DS4' : 311,
	'EB4' : 311,
	'E4' : 330,
	'F4' : 349, 'FS4' : 370,
	'G4' : 392, 'GS4' : 415,
	'A4' : 440, 'AS4' : 466,
	'BB4' : 466,
	'B4' : 494,
	'C5' : 523, 'CS5' : 554,
	'D5' : 587, 'DS5' : 622,
	'EB5' : 622,
	'E5' : 659,
	'F5' : 698, 'FS5' : 740,
	'G5' : 784, 'GS5' : 831,
	'A5' : 880, 'AS5' : 932,
	'BB5' : 932,
	'B5' : 988,
	'C6' : 1047, 'CS6' : 1109,
	'D6' : 1175, 'DS6' : 1245,
	'EB6' : 1245,
	'E6' : 1319,
	'F6' : 1397, 'FS6' : 1480,
	'G6' : 1568, 'GS6' : 1661,
	'A6' : 1760, 'AS6' : 1865,
	'BB6' : 1865,
	'B6' : 1976,
	'C7' : 2093, 'CS7' : 2217,
	'D7' : 2349, 'DS7' : 2489,
	'EB7' : 2489,
	'E7' : 2637,
	'F7' : 2794, 'FS7' : 2960,
	'G7' : 3136, 'GS7' : 3322,
	'A7' : 3520, 'AS7' : 3729,
	'BB7' : 3729,
	'B7' : 3951,
	'C8' : 4186, 'CS8' : 4435,
	'D8' : 4699, 'DS8' : 4978
}

melody = [
  notes['E7'], notes['E7'], 0, notes['E7'],
  0, notes['C7'], notes['E7'], 0,
  notes['G7'], 0, 0,  0,
  notes['G6'], 0, 0, 0,
 
  notes['C7'], 0, 0, notes['G6'],
  0, 0, notes['E6'], 0,
  0, notes['A6'], 0, notes['B6'],
  0, notes['AS6'], notes['A6'], 0,
 
  notes['G6'], notes['E7'], notes['G7'],
  notes['A7'], 0, notes['F7'], notes['G7'],
  0, notes['E7'], 0, notes['C7'],
  notes['D7'], notes['B6'], 0, 0,
 
  notes['C7'], 0, 0, notes['G6'],
  0, 0, notes['E6'], 0,
  0, notes['A6'], 0, notes['B6'],
  0, notes['AS6'], notes['A6'], 0,
 
  notes['G6'], notes['E7'], notes['G7'],
  notes['A7'], 0, notes['F7'], notes['G7'],
  0, notes['E7'], 0, notes['C7'],
  notes['D7'], notes['B6'], 0, 0
]
tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
]


underworld_melody = [
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0, notes['DS4'], notes['CS4'], notes['D4'],
  notes['CS4'], notes['DS4'],
  notes['DS4'], notes['GS3'],
  notes['G3'], notes['CS4'],
  notes['C4'], notes['FS4'], notes['F4'], notes['E3'], notes['AS4'], notes['A4'],
  notes['GS4'], notes['DS4'], notes['B3'],
  notes['AS3'], notes['A3'], notes['GS3'],
  0, 0, 0
]

underworld_tempo = [
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  6, 18, 18, 18,
  6, 6,
  6, 6,
  6, 6,
  18, 18, 18, 18, 18, 18,
  10, 10, 10,
  10, 10, 10,
  3, 3, 3
]

final_countdown_melody = [
	notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['B4'],notes['C5'],notes['D5'],notes['C5'],notes['D5'],
	notes['E5'],notes['D5'],notes['C5'],notes['B4'],notes['A4'],notes['F5'],
	notes['E5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['E5'],
]

final_countdown_tempo = [
	1,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,4,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,16,16,4,16,16,
	8,8,8,8,4,4,
	2,8,4,16,16,
	1,
]

zero_melody = [
        notes['A3']
]

zero_tempo = [
        1,
]


one_melody = [
	notes['A3']
]

one_tempo = [
	1,
]

two_melody = [
	notes['B3']
]

two_tempo = [
	1,
]

three_melody = [
	notes['C3']
]

three_tempo = [
	1,
]

four_melody = [
	notes['A4']
]

four_tempo = [
	1,
]

five_melody = [
	notes['B4']
]

five_tempo = [
	1,
]

six_melody = [
	notes['C4']
]

six_tempo = [
	1,
]

seven_melody = [
	notes['A5']
]

seven_tempo = [
	1,
]

eight_melody = [
	notes['B5']
]

eight_tempo = [
	1,
]

nine_melody = [
        notes['C5']
]

nine_tempo = [
        1,
]

star_wars_melody = [ 
	notes['G4'], notes['G4']
]


star_wars_tempo = [
	2, 2
]

#GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
GPIO.setup(Buzzer_Pin, GPIO.OUT)
GPIO.output(Buzzer_Pin, GPIO.HIGH)

def on():
	GPIO.output(Buzzer_Pin, GPIO.LOW)

def off():
	GPIO.output(Buzzer_Pin, GPIO.HIGH)

def beep(x):
	on()
	time.sleep(x)
	off()
	time.sleep(x)

def correct_passcode_entered():
    rgb.set_color(GREEN)
    print("Passcode accepted. Access granted.")
    print "Super Mario Theme"
    play(melody, tempo, 1.3, 0.800)
    time.sleep(10)
#    time.sleep(8)
    cleanup()
    sys.exit()

def incorrect_passcode_entered():
    global counter, entered_passcode
    rgb.set_color(RED)
    play(star_wars_melody, star_wars_tempo, 0.50, 1.000)
    time.sleep(1)
    rgb.set_color(BLUE)
    print("Incorrect passcode. Access denied.")
    #cleanup()
    entered_passcode = entered_passcode[:-4]
    counter = counter + 1
    if counter > 3:
	GPIO.setup(Relay_Pin, GPIO.OUT)
	#print "The Final Countdown"
	#play(final_countdown_melody, final_countdown_tempo, 0.30, 1.2000)
    	#time.sleep(25)
     #sys.exit()

def digit_entered(key):
    global entered_passcode, correct_passcode

    entered_passcode += str(key)
    print(entered_passcode)

    if len(entered_passcode) == len(correct_passcode):
    	if entered_passcode == correct_passcode:
            correct_passcode_entered()
    	else:
            incorrect_passcode_entered()

def digit_entered2(key):
    global passcode, correct_passcode

    passcode += str(key)
    print(passcode)

    if len(entered_passcode) == len(correct_passcode):
	rgb.set_color(BLUE)
	print("PASSCODE: SET", passcode)
#    	if entered_passcode == correct_passcode:
#            correct_passcode_entered()
#    	else:
#            incorrect_passcode_entered()


def digit_entered3(key):
    global timer#, correct_passcode

    timer += str(key)
    print(timer)

    if len(timer) == len(correct_passcode):
	rgb.set_color(WHITE)
	print("Time: SET", timer)
#    	if entered_passcode == correct_passcode:
#            correct_passcode_entered()
#    	else:
#            incorrect_passcode_entered()

def key_pressed3(key):
    try:
        int_key = int(key)
	if int_key >= 0 and int_key <= 9:
	     if int_key == 0:
                play(zero_melody, zero_tempo, 0.30, .2000)
             if int_key == 1:
             	play(one_melody, one_tempo, 0.30, .2000)
             if int_key == 2:
             	play(two_melody, two_tempo, 0.30, .2000)
             if int_key == 3:
             	play(three_melody, three_tempo, 0.30, .2000)
             if int_key == 4:
             	play(four_melody, four_tempo, 0.30, .2000)
             if int_key == 5:
             	play(five_melody, five_tempo, 0.30, .2000)
             if int_key == 6:
             	play(six_melody, six_tempo, 0.30, .2000)
             if int_key == 7:
             	play(seven_melody, seven_tempo, 0.30, .2000)
             if int_key == 8:
             	play(eight_melody, eight_tempo, 0.30, .2000)
             if int_key == 9:
             	play(nine_melody, nine_tempo, 0.30, .2000)
	     digit_entered3(key)
    except ValueError:
        non_digit_entered(key)


def non_digit_entered(key):
    global entered_passcode

    if key == "*" and len(entered_passcode) > 0:
        entered_passcode = entered_passcode[:-1]
        print(entered_passcode)

def key_pressed(key):
    try:
        int_key = int(key)
	if int_key >= 0 and int_key <= 9:
	     if int_key == 0:
                play(zero_melody, zero_tempo, 0.30, .2000)
             if int_key == 1:
             	play(one_melody, one_tempo, 0.30, .2000)
             if int_key == 2:
             	play(two_melody, two_tempo, 0.30, .2000)
             if int_key == 3:
             	play(three_melody, three_tempo, 0.30, .2000)
             if int_key == 4:
             	play(four_melody, four_tempo, 0.30, .2000)
             if int_key == 5:
             	play(five_melody, five_tempo, 0.30, .2000)
             if int_key == 6:
             	play(six_melody, six_tempo, 0.30, .2000)
             if int_key == 7:
             	play(seven_melody, seven_tempo, 0.30, .2000)
             if int_key == 8:
             	play(eight_melody, eight_tempo, 0.30, .2000)
             if int_key == 9:
             	play(nine_melody, nine_tempo, 0.30, .2000)
	     digit_entered(key)
    except ValueError:
        non_digit_entered(key)

def key_pressed2(key):
    try:
        int_key = int(key)
	if int_key >= 0 and int_key <= 9:
	     if int_key == 0:
                play(zero_melody, zero_tempo, 0.30, .2000)
             if int_key == 1:
             	play(one_melody, one_tempo, 0.30, .2000)
             if int_key == 2:
             	play(two_melody, two_tempo, 0.30, .2000)
             if int_key == 3:
             	play(three_melody, three_tempo, 0.30, .2000)
             if int_key == 4:
             	play(four_melody, four_tempo, 0.30, .2000)
             if int_key == 5:
             	play(five_melody, five_tempo, 0.30, .2000)
             if int_key == 6:
             	play(six_melody, six_tempo, 0.30, .2000)
             if int_key == 7:
             	play(seven_melody, seven_tempo, 0.30, .2000)
             if int_key == 8:
             	play(eight_melody, eight_tempo, 0.30, .2000)
             if int_key == 9:
             	play(nine_melody, nine_tempo, 0.30, .2000)
	     digit_entered2(key)
    except ValueError:
        non_digit_entered(key)

def key_pressed3(key):
    try:
        int_key = int(key)
	if int_key >= 0 and int_key <= 9:
	     if int_key == 0:
                play(zero_melody, zero_tempo, 0.30, .2000)
             if int_key == 1:
             	play(one_melody, one_tempo, 0.30, .2000)
             if int_key == 2:
             	play(two_melody, two_tempo, 0.30, .2000)
             if int_key == 3:
             	play(three_melody, three_tempo, 0.30, .2000)
             if int_key == 4:
             	play(four_melody, four_tempo, 0.30, .2000)
             if int_key == 5:
             	play(five_melody, five_tempo, 0.30, .2000)
             if int_key == 6:
             	play(six_melody, six_tempo, 0.30, .2000)
             if int_key == 7:
             	play(seven_melody, seven_tempo, 0.30, .2000)
             if int_key == 8:
             	play(eight_melody, eight_tempo, 0.30, .2000)
             if int_key == 9:
             	play(nine_melody, nine_tempo, 0.30, .2000)
	     digit_entered3(key)
    except ValueError:
        non_digit_entered(key)

#rgb.set_color(BLUE)

try:
    keypad.registerKeyPressHandler(key_pressed3)
    while len(timer) != 4:
        print(timer)
    keypad.unregisterKeyPressHandler(key_pressed3)
    #enterCode()
    #factory = rpi_gpio.KeypadFactory()
    #keypad = factory.create_4_by_3_keypad() # makes assumptions about keypad layout and GPIO pin numbers
    keypad.registerKeyPressHandler(key_pressed2)
    while len(passcode) != 4:
	print("Enter Passcode")
    correct_passcode = passcode
    keypad.unregisterKeyPressHandler(key_pressed2)
    keypad.registerKeyPressHandler(key_pressed)
    rgb.set_color(BLUE)
    print("Enter your passcode (hint: {0}).".format(correct_passcode))
    print("Press * to clear previous digit.")
    on()
    #rgb.set_color(BLUE)
    while counter <= 4:
        #rgb.set_color(BLUE)
	if usbDisarm != 1:
	    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
	    df = subprocess.check_output("lsusb")
	    devices = []
	    for i in df.split('\n'):
    	        if i:
                    info = device_re.match(i)
                if info:
                    dinfo = info.groupdict()
            #    print(dinfo)
                if "Phison Electronics Corp. Flash Disk" in str(dinfo):
                    print("YES")
		    usbDisarm = 1
		    rgb.set_color(GREEN)
		    print "Super Mario Underworld Theme"
		    play(underworld_melody, underworld_tempo, 1.3, 0.800)
   		    #for x in range(50):
		    #	rgb.set_color(GREEN)
		    #time.sleep(15)
		    cleanup()
            	dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
            	devices.append(dinfo)
	if usbDisarm == 1:
	    rgb.set_color(GREEN)
	    time.sleep(5)
	if counter == 4:
	    rgb.set_color(RED)
	    GPIO.setup(Relay_Pin, GPIO.OUT)
	    print "The Final Countdown"
	    play(final_countdown_melody, final_countdown_tempo, 0.30, 1.2000)
	    counter = counter + 1
except KeyboardInterrupt:
    print("Goodbye")
finally:
   # if counter == 3:
    #    print "The Final Countdown"
     #   play(final_countdown_melody, final_countdown_tempo, 0.30, 1.2000)
        #time.sleep(20)
    cleanup()
    #restart_program()
