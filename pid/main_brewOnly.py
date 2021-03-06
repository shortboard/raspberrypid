# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import os
import board
import digitalio
import adafruit_max31855
import gpiozero
import PID

# Setup Connection
print(dir(board))
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi, cs)

# Setup Relay
brewRelay = gpiozero.OutputDevice(23, active_high=True, initial_value=False)
steamRelay = gpiozero.OutputDevice(24, active_high=True, initial_value=False)

# Setup PID
brewTargetT = 101
steamTargetT = 120
P = 3.4
I = 0.3
D = 40.0
cycleSeconds = 1

brewPID = PID.PID(P, I, D)
brewPID.SetPoint = brewTargetT
brewPID.setSampleTime(cycleSeconds)

def readConfig():
    global brewTargetT
    global steamTargetT
    global cycleSeconds
    with open ('/config/pid.conf', 'r') as f:
        config = f.readline().split(',')
        brewPID.SetPoint = float(config[0])
        brewTargetT = brewPID.SetPoint
        brewPID.setKp (float(config[2]))
        brewPID.setKi (float(config[3]))
        brewPID.setKd (float(config[4]))
        cycleSeconds = (int(config[5]))
        brewPID.setSampleTime(cycleSeconds)

def createConfig():
#	if not os.path.isfile('/config/pid.conf'):
		with open ('/config/pid.conf', 'w') as f:
			f.write('%s,%s,%s,%s,%s,%s'%(brewTargetT,steamTargetT,P,I,D,cycleSeconds))

createConfig()

while True:
    readConfig()

    #Get temp
    tempC = max31855.temperature

    brewPID.update(tempC)
    brewTargetPwm = brewPID.output
    brewTargetPwm = max(min(int(brewTargetPwm), 100), 0)

    steamTargetPwm = 0

    print("Current: {} C | Brew Target: {} C | Steam Target: {} C | Brew PWM: {} | Steam PWM: {}".format(tempC, brewTargetT, steamTargetT, brewTargetPwm, steamTargetPwm))

    brewOnTime = (brewTargetPwm / 100.0) * cycleSeconds

    if brewOnTime != 0:
        print("Turn brew on for {} seconds".format(brewOnTime))
        brewRelay.on()

    if brewOnTime != 100:
        print("Turn brew on for {} seconds".format(brewOnTime))
        brewRelay.on()

