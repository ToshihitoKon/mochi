#!/usr/bin/env bash

cd `dirname $0`

git pull origin master
sudo systemctl restart mochi
