#!/usr/bin/env bash

cd `dirname $0`

git log --oneline | wc -l
