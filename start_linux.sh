#!/bin/bash

# Function to print error messages
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Create and activate virtual environment if it doesn't exist
if [ ! -d "Otrace_venv" ]; then
    python3 -m venv Otrace_venv || error_exit "Failed to create virtual environment."
fi

# Activate the virtual environment
source Otrace_venv/bin/activate || error_exit "Failed to activate virtual environment."

# Install dependencies
pip install --upgrade pip || error_exit "Failed to upgrade pip."
# Install required packages
required_packages=(
    bcrypt
    textual
    textual_textarea
    requests
    readline
    maskpass
)

for package in "${required_packages[@]}"; do
    pip install "$package" || error_exit "Failed to install package: $package."
done

# Upgrade outdated packages if any
outdated_packages=$(pip list --outdated --format=freeze | awk -F '==' '{print $1}')
if [ -n "$outdated_packages" ]; then
    echo "Upgrading outdated packages:"
    echo "$outdated_packages" | xargs -n1 pip install --upgrade || error_exit "Failed to upgrade some packages."
else
    echo "All packages are up to date."
fi

echo "Setup completed successfully."