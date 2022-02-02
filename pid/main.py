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

steamPID = PID.PID(P, I, D)
steamPID.SetPoint = steamTargetT
steamPID.setSampleTime(cycleSeconds)

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

        steamPID.SetPoint = float(config[1])
        steamTargetT = steamPID.SetPoint
        steamPID.setKp (float(config[2]))
        steamPID.setKi (float(config[3]))
        steamPID.setKd (float(config[4]))

        cycleSeconds = (int(config[5]))
        brewPID.setSampleTime(cycleSeconds)
        steamPID.setSampleTime(cycleSeconds)

def createConfig():
	if not os.path.isfile('/config/pid.conf'):
		with open ('/config/pid.conf', 'w') as f:
			f.write('%s,%s,%s,%s,%s,%s'%(brewTargetT,steamTargetT,P,I,D,cycleSeconds))

createConfig()

while True:
    readConfig()

    #Get temp
    try:
        tempC = max31855.temperature
    except RuntimeError:
        print("Runtime Error")
    else: # Only update values if we got a new reading, otherwise continue with current settings
        brewPID.update(tempC)
        brewTargetPwm = brewPID.output
        brewTargetPwm = max(min(int(brewTargetPwm), 100), 0)

        steamPID.update(tempC)
        steamTargetPwm = steamPID.output
        steamTargetPwm = max(min(int(steamTargetPwm), 100), 0)

    print("Current: {} C | Brew Target: {} C | Steam Target: {} C | Brew PWM: {} | Steam PWM: {}".format(tempC, brewTargetT, steamTargetT, brewTargetPwm, steamTargetPwm))

    brewOnTime = (brewTargetPwm / 100.0) * cycleSeconds
    steamOnTime = (steamTargetPwm / 100.0) * cycleSeconds

    if brewOnTime != 0:
        brewRelay.on()
    if steamOnTime != 0:
        steamRelay.on()

    first = min(brewOnTime, steamOnTime)
    second = max(brewOnTime, steamOnTime) - first
    third = cycleSeconds - max(brewOnTime, steamOnTime)

    print("Brew on for {} seconds, steam on for {} more seconds, both off for {} seconds".format(first, second, third))
    time.sleep(first)
    if (brewTargetPwm != 100):
        brewRelay.off()
    
    time.sleep(second)
    if (steamTargetPwm != 100):
        steamRelay.off()
    
    time.sleep(third)