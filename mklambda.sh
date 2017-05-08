#!/bin/bash

rm -rf auto_lottery_lambda.zip
zip -9 $HAMILTON_LOTTERY_HOME/auto_lottery_lambda.zip
cd ~/.virtualenvs/hammy/lib/python2.7/site-packages
zip -r9 $HAMILTON_LOTTERY_HOME/auto_lottery_lambda.zip *
cd -
zip -r9 $HAMILTON_LOTTERY_HOME/auto_lottery_lambda.zip phantomjs
zip -g auto_lottery_lambda.zip auto_lottery.py
