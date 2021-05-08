#!/bin/bash
# First time install for carbonhat
#On a Raspberry Pi with Sense HAT board
#starting with fresh RaspiOS SD card image

# Todo: don't assume /home/pi/carbonhat, use the actual path

#sudo apt-get update

# don't reinstall these if already installed

dpkg -s python3-venv | grep -q "ok installed" || sudo apt-get install python3-venv
dpkg -s sense-hat | grep -q "ok installed" || sudo apt-get install sense-hat
#(you will have to reboot to make Sense HAT functional)

#(Create a virtual environment, I love these for organising my Python stuff)
#(system-site-packages option is needed to pick up the sense-hat package)
if ! [ -e ./venv ]
then
    python3 -m venv --system-site-packages venv
    source venv/bin/activate
    pip install requests
fi

chmod u+x run.sh

# Make simple systemd script to run the carbonhat
# Note, we can use the virtual environment without activating it,
# by using its Python interpreter explicitly
# https://stackoverflow.com/questions/37211115/how-to-enable-a-virtualenv-in-a-systemd-service-unit etc
sudo tee /etc/systemd/system/carbonhat.service >/dev/null <<EOF
[Unit]
Description=Carbon intensity display
After=network.target
StartLimitIntervalSec=0
[Service]
Type=simple
Restart=always
RestartSec=30
User=pi
WorkingDirectory=/home/pi/carbonhat
ExecStart=/home/pi/carbonhat/venv/bin/python -u /home/pi/carbonhat/carbonhat.py

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable carbonhat
