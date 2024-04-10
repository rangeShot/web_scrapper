#!/bin/bash

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
#for mac os / linux
source venv/bin/activate
#for windows
# . venv/Scripts/activate

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

echo "Environment setup complete."

# Run the Python application
echo "Running the application now"
python3 app.py