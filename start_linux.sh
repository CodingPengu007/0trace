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
    textual==0.89.1
    textual_textarea==0.15.0
    requests
    maskpass
    # readline
)

for package in "${required_packages[@]}"; do
    if [ "$package" == "readline" ]; then
        echo "Skipping installation of readline via pip. Ensure 'libreadline-dev' is installed on your system."
        continue
    fi
    pip install "$package" || error_exit "Failed to install package: $package."
done

# Upgrade outdated packages except textual and textual_textarea
outdated_packages=$(pip list --outdated --format=columns | awk 'NR>2 {print $1}' | grep -Ev '^(textual|textual_textarea)$')
if [ -n "$outdated_packages" ]; then
    echo "Upgrading outdated packages (excluding textual and textual_textarea):"
    echo "$outdated_packages" | xargs -n1 pip install --upgrade || error_exit "Failed to upgrade some packages."
else
    echo "All packages are up to date (excluding textual and textual_textarea)."
fi

echo "Setup completed successfully."