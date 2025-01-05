#!/bin/bash

# Check Python version
source ./check_python.sh

# If Python version check passes, install requirements
if [ $? -eq 0 ]; then
    echo "Installing required packages..."
    python3 -m pip install -r requirements.txt
    echo "Setup complete! You can now run: python3 simple_reconcile.py"
else
    exit 1
fi 