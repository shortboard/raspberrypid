# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import os
import board
import digitalio
import adafruit_max31855
import PID

# Setup Connection
print(dir(board))
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi, cs)

# Setup PID
targetT = 35
P = 10
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

def readConfig ():
	global targetT
	with open ('/config/pid.conf', 'r') as f:
		config = f.readline().split(',')
		pid.SetPoint = float(config[0])
		targetT = pid.SetPoint
		pid.setKp (float(config[1]))
		pid.setKi (float(config[2]))
		pid.setKd (float(config[3]))

def createConfig ():
	if not os.path.isfile('/config/pid.conf'):
		with open ('/config/pid.conf', 'w') as f:
			f.write('%s,%s,%s,%s'%(targetT,P,I,D))

createConfig()

while True:
    readConfig()

    #Get temp
    tempC = max31855.temperature

    pid.update(tempC)
    targetPwm = pid.output
    targetPwm = max(min(int(targetPwm), 100), 0)

    print("Current: {} C | Target: {} C | PWM: {}".format(tempC, targetT, targetPwm))

    onTime = targetPwm / 100.0

    if (targetPwm != 0):
        print("Turn on for {} seconds".format(onTime))
        time.sleep(onTime)
    
    if (targetPwm != 100):
        print("Turn off for {} seconds".format(1 - onTime))
        time.sleep(1 - onTime)
    
