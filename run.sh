#!/bin/bash

echo "Setting up virtual environment..."
python3 -m venv env
echo "Activating virtual environment..."
source env/bin/activate
echo "Upgrading pip..."
env/bin/python -m pip install --upgrade pip
echo "Installing required libraries..."
pip install -r requirements.txt
echo "Installation complete."
read -p "Press any key to continue..."
