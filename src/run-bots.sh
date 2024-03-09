#!/bin/bash

python3 main.py --logic Padibot --email=test@email.com --name=padibot --password=123456 --team etimo &
python3 main.py --logic attackBot --email=test1@email.com --name=attack --password=123456 --team etimo &
python3 main.py --logic attackBot --email=test2@email.com --name=stima2 --password=123456 --team etimo &
python3 main.py --logic attackBot --email=test3@email.com --name=stima3 --password=123456 --team etimo &