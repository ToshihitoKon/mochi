#!/usr/bin/env bash
rootdir=`dirname $0`

export FLASK_APP="${rootdir}/src/main.py"
export FLASK_ENV="production"
python3 -m flask run --host=0.0.0.0
