#!/bin/bash

# Required Python version
REQUIRED_VERSION="3.8"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python ${REQUIRED_VERSION} or higher"
    exit 1
fi

# Check Python version
if ! python3 -c "import sys; assert sys.version_info >= tuple(map(int, '${REQUIRED_VERSION}'.split('.'))), f'Python {${REQUIRED_VERSION}} or higher is required'" 2> /dev/null; then
    echo "Python ${REQUIRED_VERSION} or higher is required"
    echo "Current version: $(python3 -V)"
    exit 1
fi

echo "Python version check passed"
exit 0 