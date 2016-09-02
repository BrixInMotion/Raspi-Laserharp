import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

enablepin = 23
clockpin = 4
directionpin = 18
half_full_pin = 17
controllpin = 27
Ls_pin = 22

beams = 4           #How many beams
singlestep = 5      #How many Steps between the beams

GPIO.setup(enablepin, GPIO.OUT)
GPIO.setup(clockpin, GPIO.OUT)
GPIO.setup(directionpin, GPIO.OUT)
GPIO.setup(half_full_pin, GPIO.OUT)
GPIO.setup(controllpin, GPIO.OUT)
GPIO.setup(Ls_pin, GPIO.IN)

GPIO.output(enablepin, GPIO.HIGH)
GPIO.output(half_full_pin, GPIO.HIGH)       #Halbschrittbetrieb bei High
GPIO.output(clockpin, GPIO.HIGH)
GPIO.output(controllpin, GPIO.LOW)          #langsames Abfallen der Phasenspannung bei High

def stepper(steps, direction, delay):
    GPIO.output(directionpin, direction)    #Richtung setzen   
    for i in range(0, steps):
        GPIO.output(clockpin, GPIO.LOW)
        time.sleep(0.0009)
        #print ('high')
        GPIO.output(clockpin, GPIO.HIGH)
        time.sleep(delay)
        #print ('low')

def startposition(delay):
   stepper(50, 0, delay)
   while GPIO.input(Ls_pin) == 0:
      stepper(1, 0, delay)
   stepper(4, 0, delay)

def auffaechern(steps, beams):
    for i in range(0, steps):
        for o in range(10):
            for k in range(0,beams):
                stepper(i, 0, 0.001)
                time.sleep(0.03)
            stepper(i*beams , 1, 0.001)
            

try:
    startposition(0.001)
    #auffaechern(singlestep, beams)                 #Experimental
    while (True):
        for i in range (0, beams):
            stepper(singlestep, 0, 0.0009)         # stepper(steps, direction, delay)
            time.sleep(0.03)
        stepper(beams*singlestep, 1, 0.0009)
except KeyboardInterrupt:
    GPIO.output(enablepin, GPIO.LOW)
        
