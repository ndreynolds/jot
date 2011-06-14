#!/usr/bin/bash

# A short script to reinstall jot for testing purposes

echo "Removing old installation."
rm -rf ~/.jot
python setup.py
