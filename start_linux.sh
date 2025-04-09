#!/bin/bash

# Function to print error messages
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    error_exit "python3 could not be found. Please install Python 3."
fi

# Check if pip is installed
if ! python3 -m pip --version &> /dev/null; then
    error_exit "pip could not be found. Please install pip for Python 3."
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "Otrace_venv" ]; then
    python3 -m venv Otrace_venv || error_exit "Failed to create virtual environment."
fi

# Activate the virtual environment
source Otrace_venv/bin/activate || error_exit "Failed to activate virtual environment."

# Install dependencies
pip install --upgrade pip || error_exit "Failed to upgrade pip."
pip install bcrypt texteditor || error_exit "Failed to install required packages."

# Upgrade outdated packages if any
outdated_packages=$(pip list --outdated --format=freeze | awk -F '==' '{print $1}')
if [ -n "$outdated_packages" ]; then
    echo "Upgrading outdated packages:"
    echo "$outdated_packages" | xargs -n1 pip install --upgrade || error_exit "Failed to upgrade some packages."
else
    echo "All packages are up to date."
fi

echo "Setup completed successfully."