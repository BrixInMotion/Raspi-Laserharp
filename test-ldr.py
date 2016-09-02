#
#A small program to scan the light intensity with an ldr and a capacitor
#Typical values are around 3000 in darkness, and around 200 with a bit light
#

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

measurepinpin = 24

def rc_time(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.0001)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
    return count

intensity = 0 
while True:
    try:
        for k in range(3):
            intensity = intensity + rc_time(measurepin)
        intensity = intensity/3
        print (int(intensity))
        time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
