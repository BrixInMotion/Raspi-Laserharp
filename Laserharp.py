#
#2016-09-02
#copyright (c) 2016, BrixInMotion
#

import RPi.GPIO as GPIO
import time
import string
from psonic import *
import sys
#---------------------Setup-L297----------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

enablepin = 23
clockpin = 4
directionpin = 18
half_full_pin = 17
controllpin = 27
Ls_pin = 22
photosensor = 24

GPIO.setup(enablepin, GPIO.OUT)
GPIO.setup(clockpin, GPIO.OUT)
GPIO.setup(directionpin, GPIO.OUT)
GPIO.setup(half_full_pin, GPIO.OUT)
GPIO.setup(controllpin, GPIO.OUT)
GPIO.setup(Ls_pin, GPIO.IN)
GPIO.setup(photosensor, GPIO.IN)

GPIO.output(enablepin, GPIO.HIGH)
GPIO.output(half_full_pin, GPIO.HIGH)       #Halbschrittbetrieb bei High
GPIO.output(clockpin, GPIO.HIGH)
GPIO.output(controllpin, GPIO.LOW) #langsames Abfallen der Phasenspannung bei High

#----------------Setup-Variables----------------------------------
level = 3000                #in darkness 3000, by light around 200
intensity = 0
beams = 3                  #How many beams (1-7)
singlestep = 7             #How many steps are between the beams (beams * singlestep should be around 20)
controlrun = 1
liste = [" . "," . "," . "," . "," . "," . "," . "]

run = list(range(0, 3))
run[0] = [0,0,0,0,0,0,0]
run[1] = [0,0,0,0,0,0,0]
run[2] = [0,0,0,0,0,0,0]

use_synth(PROPHET)                      #Synth-Sound: PROPHET, SAW, etc.
notes = [C4, D4, E4, F4, G4, A4, B4]    #note-pattern
#notes = [Gs4, G4, F4, C4]              #note-pattern for imitationgame

#--------------------functions---------------------------------
def stepper(steps, direction, delay):
    GPIO.output(directionpin, direction)    #Richtung setzen   
    for i in range(0, steps):
        GPIO.output(clockpin, GPIO.LOW)
        time.sleep(0.001)
        #print ('high')
        GPIO.output(clockpin, GPIO.HIGH)
        time.sleep(delay)
        #print ('low')

def measure(pin):
   global count
   count = 0
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)
   time.sleep(0.00001)
   GPIO.setup(pin, GPIO.IN)
   while (GPIO.input(pin) == GPIO.LOW) and count < level:
      count += 1
      #print count
   return count
    

def playmusic():
   for i in range(0,beams):
      if run[0] [i] == 1:         #if run[0] [i] and run[1] [i] and run[2] [i] == 1:
         play(notes[i], attack=0.5, sustain=0.5, release=0.5)   # attack=0.5, sustain=0.5, release=0.5


def printf(onoff, note, runner):
   if onoff == 1:
      liste[note] = " 0 "
      run[runner] [note] = 1
   else:
      liste[note] = " . "
      run[runner] [note] = 0
   if note == 0:
      print("".join(liste))
      #print liste

def scan(position):
    #Laser an
    time.sleep(0.002)
    for k in range(10):
      intensity = intensity + measure(Ls_pin)
    intensity = intensity/10
    if intensity < level:         #Ton spielen bzw stoppen
        #play(1, i)
        printf(1,position)
    else:
        #play(0, i)
        printf(0,position)
    #Laser aus

def startposition(delay):
   stepper(50, 0, delay)
   while GPIO.input(Ls_pin) == 0:
      stepper(1, 0, delay)
   #stepper(2, 0, delay)
   print ('Mirror is in startposition')

def levelintensity():
    global level
    global intensity
    intensity = 0
    print('> Scanning background light, dont touch the beam! (Hit ENTER)')     #Scan backgroundlight
    while input() != "":
        time.sleep(0.1)
    for k in range(100):
        intensity = intensity + measure(photosensor)
    backgroundlight = intensity/100
    intensity = 0
    print('Backgroundlight: {}'.format(backgroundlight))

    print('')
    print('> Now touch the beam! (Hit ENTER)')                           #Scan Reflectionlight
    while input() != "":
        time.sleep(0.1)
    for k in range(100):
        intensity = intensity + measure(photosensor)
    reflectionlight = intensity/100
    intensity = 0
    print('Reflectionlight: {}'.format(reflectionlight))
                                                        #calculate the middle
    level = ((backgroundlight - reflectionlight)/2) + reflectionlight
    print('Level:           {}'.format(level))
    print('Hit ENTER to continue or S to scan once more!')
    if input() == "s":
        level = 3000
        levelintensity()
        
    

if __name__ == '__main__':
   try:
      startposition(0.001)          #uncomment this if you have no light barrier or if you bring your stepper manually in startposition
      levelintensity()              #callibrates the intensity-level
      print('-----------')
      print('Starting...')
      print('-----------')
      while True:
         for a in range (0,controlrun):
            for i in range(0,beams):
               stepper(singlestep, 0, 0.0001)
               #time.sleep(0.01)
               for k in range(5):
                  intensity = intensity + measure(photosensor)
               intensity = intensity/5
               if intensity < level:
                  printf(1,i,a)
               else:
                  printf(0,i,a)
            stepper(singlestep*beams, 1, 0.0001)
         playmusic()

   except KeyboardInterrupt:
      GPIO.output(enablepin, GPIO.LOW)
      print (' Set enablepin to LOW')
      GPIO.cleanup()
