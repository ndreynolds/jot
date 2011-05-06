#!/usr/bin/bash

# A short script to reinstall todo for testing purposes

echo "Removing old installation."
rm -rf ~/.todo
python setup.py
