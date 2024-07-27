#!/bin/env bash

FILE=".installed"
if [ ! -f "$FILE" ]; then
    sudo apt update
    sudo apt install python3 python-is-python3 python3-venv python3-pip php php-cgi php-mysql php-xml
    sudo pip3 install -r requirements.txt
    chmod +x run.sh
    echo "Installation complete" > .installed
else
    echo "Already installed"
fi
bash run.sh
