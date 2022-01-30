# RaspberryPID
Modification i'm making for my Rancillio Silvia coffee machine due to killing one of the thermostats by leaving it on for an extended period of time. It uses a RPi Zero W 2, a K type thermocouple with a MAX31855K thermocouple interface and a couple of relays to get more accurate and stable temparatures while brewing.

This is built using whatever tech i need (currently python) and contained in docker containers that i'm deploying to the Pi using Balena (though it should work fine in any distro with a docker host). 

# Future Features
- Auto sleep (incase i leave the coffee machine on too long again)
- Scheduler / Remote wakeup
- Web portal configuration (though i might host that on azure in docker containers)

# Pi in the sky features
- Shot timer (will need to change the hardware setup so this probably wont happen)
