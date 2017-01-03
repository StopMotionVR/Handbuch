#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import sys
import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

	atexit.register(turnOffMotors)

speed = int(sys.argv[1])
steps = int(sys.argv[2])
direction = int(sys.argv[3])
step_type = int(sys.argv[4])

# step count issn't used by the library ... dunno why!?
myStepper = mh.getStepper(200, 1)
myStepper.setSpeed(speed)
myStepper.step(steps, direction, step_type)
