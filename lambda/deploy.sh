#!/bin/bash

CWD=$(pwd)
cd $(dirname "$0")
python3 -m pip -q install -t ./package -r requirements.txt
rm -f deployment-pkg.zip
cd package
zip -qr ../deployment-pkg.zip .
cd ..
rm -rf package
zip -qg deployment-pkg.zip bot.py .key
cd $CWD