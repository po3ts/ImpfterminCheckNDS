#!/bin/bash

CWD=$(pwd)
cd $(dirname "$0")
python3 -m pip install -t ./package -r requirements.txt
cd package
zip -r ../deployment-pkg.zip .
cd ..
zip -g deployment-pkg.zip bot.py .key
cd $CWD