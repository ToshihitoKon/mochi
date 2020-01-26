#!/usr/bin/env bash

export FLASK_APP="/home/pi/mochi/src/main.py"
export FLASK_ENV="production"
python3 -m flask run --host=0.0.0.0
