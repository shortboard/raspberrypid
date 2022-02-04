# RaspberryPID
*Ever wanted to turn your coffee machine into a docker host?*

This is a quick collection of docker containers i've put together to get a PID running on my Rancilio Silvia. It's currently able to control both steam and brew temperature. The wiring is pretty simple so i haven't drawn it up yet but the basic premise is:

Thermocouple --via SPI0--> Pi Zero W 2 --via GPIO 23/24--> 2 Relays (Switching where the existing thermostats were connected to the circuit.)
               

# Current Features
- Brew temperature control
- Steam temperature control

## Hardware
- [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [MAX31855 Breakout](https://core-electronics.com.au/thermocouple-amplifier-max31855-breakout-board-max6675-upgrade-v2-0.html)
- [Type K Thermocouple](https://www.auberins.com/index.php?main_page=product_info&products_id=307)
- [Relays](https://core-electronics.com.au/solid-state-relay-40a-3-32v-dc-input.html)

## Future features
- Configuration API
- Redis temperature history (Redis has a cool timeseries mode that would be good for this, not built for ARM so i'll have to build it myself)
- Auto sleep (incase i leave the coffee machine on too long again)
- Scheduler / Remote wakeup
- Web portal configuration (though i might host that on azure in docker containers)

## Pi in the sky features
- Shot timer (will need to change the hardware setup so this probably wont happen)
- Pre-infusion (wonder if i can achieve this by just opening the brew valve without the pump?)
