#!/bin/bash

FILE=".env_var"
if [ ! -f "$FILE" ]; then
    sudo apt update
    sudo apt install python3
    sudo apt-get install python3 python3-venv python3-pip php php-cgi php-mysql php-xml
    # python3 -m venv honeypot-env
    sudo pip3 install -r requirements.txt
    chmod +x run.sh
    echo "Installation complete" > .env_var
else
    echo "Already installed"
    bash run.sh
fi
