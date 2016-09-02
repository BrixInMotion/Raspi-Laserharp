#
#To run the program, copy psonic.py in the same folder like this
#and start Sonic-Pi. Then start this program with python3 and
# - press a key between a and h for the different notes
# - press a number between 1 and 6 for the different synths
# then press Enter
#

from psonic import *
from threading import Thread
import time
import sys

def loop():
    while True:
        sample(DRUM_SNARE_SOFT)
        sleep(0.5)


while (True):
    a = sys.stdin.read(1)
    if a == "1":
        use_synth(SAW)
    elif a == "2":
        use_synth(PROPHET)
    elif a == "3":
        use_synth(DSAW)
    elif a == "4":
        use_synth(FM)
    elif a == "5":
        use_synth(TB303)
    elif a == "6":
        use_synth(PULSE)
    elif a == "a":
        play(C4, attack=1, sustain=1, release=1)
    elif a == "s":
        play(D4, attack=1, sustain=1, release=1)
    elif a == "d":
        play(E4, attack=1, sustain=1, release=1)
    elif a == "f":
        play(F4, attack=1, sustain=1, release=1)
    elif a == "g":
        play(G4, attack=1, sustain=1, release=1)
    elif a == "h":
        play(A4, attack=1, sustain=1, release=1)
    elif a == "j":
        play(B4, attack=1, sustain=1, release=1)
    elif a == "k":
        loop()

