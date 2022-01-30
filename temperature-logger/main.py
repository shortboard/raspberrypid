# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import adafruit_max31855

print(dir(board))
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)

max31855 = adafruit_max31855.MAX31855(spi, cs)
while True:
    tempC = max31855.temperature
    tempCint = max31855.reference_temperature
    tempCNIST = max31855.temperature_NIST
    tempF = tempC * 9 / 5 + 32
    print("Temperature: {} C {} F ".format(tempC, tempF))
    print("Internal Temperature: {} C".format(tempCint))
    print("NIST Temperature: {} C".format(tempC))
    time.sleep(2.0)