#!/bin/sh

# Compile the qt resources file to a python module

cd "$(dirname "$0")"

pyrcc5 icons.qrc -o muteme/icons_rc.py
