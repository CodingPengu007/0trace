# START SCRIPT
# MacOS

#!/bin/bash

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "python3 could not be found. Please install Python 3."
    exit 1
fi

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    echo "pip could not be found. Please install pip for Python 3."
    exit 1
fi

# Create and activate virtual environment
python3 -m venv Otrace_venv
source Otrace_venv/bin/activate

# Install dependencies
pip install bcrypt
pip install --upgrade pip
pip list --outdated --format=freeze | cut -d '=' -f 1 | xargs -n1 pip install --upgrade