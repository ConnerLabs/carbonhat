# Carbonhat
This was knocked together on a Saturday afternoon when I was bored and the weather was rotten :) I've been using JSON APIs at work lately, so when I saw https://api.carbonintensity.org.uk I couldn't resist!
## What does it do
**Note this is for the UK only**

It is a fun piece of physical computing that runs on a Raspberry Pi with the Sense HAT board. The Sense HAT LEDs light in a colour representing the carbon footprint of your electricity over the next 3 hours. Green means completely renewable, through yellow and orange to red which means "as bad as gas". You can use this to inform decisions about your electricity usage.

## Principle of operation

- Queries the API at https://carbonintensity.org.uk to get a carbon forecast for your region 

- Crunches it to get an average carbon intensity for your electricity for the next 3 hours

- Lights all of the LEDs on the Sense HAT board in an appropriate colour. Pure green is a carbon intensity of 0, going through yellow to pure red at a carbon intensity of 215g/kWh.

- The LEDs are dimmed between 11pm and 6am.

## How to install
Use a Raspberry Pi with a Sense HAT board and the latest RaspiOS Lite ("Raspbian Buster Lite")

Get an internet connection for it and SSH access to it from a desktop machine.

Update the package lists with sudo apt-get update.

Install Git and clone this repository.

```
cd carbonhat
./install.sh
```
Reboot and it should start automatically

## Todo
- Make an INI file so other users can enter their own postcode instead of having mine hard coded :)

- Make it actually control a dual fuel gas/electric heating system