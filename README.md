# Raspi-Laserharp

To build the Laserharp you need: <br/>
- a bipolar (4 wire) Stepper motor with a small mirror to deflect the Laserbeam <br/>
- a steppermotor-driver, for example with a L297 and L298 (the schematics can be found [here](http://www.precifast.de/schaltplan-schrittmotorsteuerung-mit-l297-und-l298/)) <br/>
- a powerful Laserpointer <br/>
- a LDR-resistor and a 1uF Capacitor <br/>
- a Raspberry Pi 3 <br/>
<br/>
First clone this repository to your Pi, and install the Software for Sonic Pi to create a sound:  <br/>
https://github.com/gkvoelkl/python-sonic <br/>

Then conect your Stepper-Driver like this: <br/>
enablepin:      GPIO 23 <br/>
clockpin:       GPIO 4 <br/>
directionpin:   GPIO 18 <br/>
half_full_pin:  GPIO 17 <br/>
controllpin:    GPIO 27 <br/>
Ls_pin:         GPIO 22 <br/>
photosensor:    GPIO 24 <br/>
 <br/>
I also used a Light barrier to bring the stepper in Startposition, but you can also uncomment startposition() in
Laserharp.py.
To test the single parts of your hardware you can use the test-x.py Programs.







