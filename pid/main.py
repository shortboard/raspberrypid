# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import os
import board
import digitalio
import adafruit_max31855
import gpiozero
import PID
import json

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
steamPID = PID.PID(P, I, D)

# Creates a default config file if one does not exist yet
def createConfig():
    if not os.path.isfile('/config/pid.config.json'):
        config = {
            "brew_target_temp": brewTargetT,
            "steam_target_temp": steamTargetT,
            "p": P,
            "i": I,
            "d": D,
            "cycle_seconds": cycleSeconds
        }
        with open ('/config/pid.config.json', 'w') as f:
            json.dump(config, f)

# reads the values from the config (does this every cycle to pick up on any config changes, though im considering reducing the reads and just updating every 30 seconds or so)
def readConfig():
    global brewTargetT
    global steamTargetT
    global cycleSeconds
    with open ('/config/pid.config.json', 'r') as f:
        config = json.load(f)
        brewPID.SetPoint = min(float(config["brew_target_temp"]), 110.0)
        brewTargetT = brewPID.SetPoint
        brewPID.setKp(float(config["p"]))
        brewPID.setKi(float(config["i"]))
        brewPID.setKd(float(config["d"]))

        steamPID.SetPoint = min(float(config["steam_target_temp"]), 140.0)
        steamTargetT = steamPID.SetPoint
        steamPID.setKp(float(config["p"]))
        steamPID.setKi(float(config["i"]))
        steamPID.setKd(float(config["d"]))

        cycleSeconds = (int(config["cycle_seconds"]))
        brewPID.setSampleTime(cycleSeconds)
        steamPID.setSampleTime(cycleSeconds)

createConfig()

while True:
    readConfig()

    #Get temp
    try:
        tempC = max31855.temperature
    except RuntimeError: # I have a issue with my thermocouple shorting to ground periodically (likely because i fried the sheath with 240v, be very careful in your coffee machine)
        print("Runtime Error")
    else: # Discard values unless we got a new reading. This means the element will be pulsed as the same rate as last cycle.
        brewPID.update(tempC)
        brewTargetPwm = brewPID.output
        brewTargetPwm = max(min(int(brewTargetPwm), 100), 0)

        steamPID.update(tempC)
        steamTargetPwm = steamPID.output
        steamTargetPwm = max(min(int(steamTargetPwm), 100), 0)

        # Store to redis here

    print("Current: {} C | Brew Target: {} C | Steam Target: {} C | Brew PWM: {} | Steam PWM: {}".format(tempC, brewTargetT, steamTargetT, brewTargetPwm, steamTargetPwm))

    # The rest of the logic is to pules the element on and off according to the Pwm values. I only pulse once per cycle incase it effects the longevity of the element.
    # This is also why you should use a solid state relay as a mechanical will fail reasonably quickly doing this many cycles (along with being incredibly noisy).
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