#!/bin/bash

cd $HAMILTON_LOTTERY_HOME
source secrets.sh
source ~/.virtualenvs/hammy/bin/activate 
python auto_lottery.py -d

