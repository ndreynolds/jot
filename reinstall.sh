#!/usr/bin/bash

# A short script to reinstall jot for testing purposes
# Run with sudo if you need to

echo "Removing old installation."
rm -rf ~/.jot
python setup.py
