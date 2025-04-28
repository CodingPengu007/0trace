# Create and activate virtual environment if it doesn't exist
if [ ! -d "Otrace_venv" ]; then
    python3 -m venv Otrace_venv

<<<<<<< HEAD
    source Otrace_venv/bin/activate
    pip install --upgrade pip

=======
    # Activate the virtual environment
    source Otrace_venv/bin/activate

    # Install dependencies
    pip install --upgrade pip

    # Install required packages
>>>>>>> c470e6e651d04d481fcd7b060a6e16d7ec3c5d8f
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
        pip install "$package"
    done
<<<<<<< HEAD

fi

=======
fi

# Activate the virtual environment
source Otrace_venv/bin/activate

>>>>>>> c470e6e651d04d481fcd7b060a6e16d7ec3c5d8f
# Upgrade outdated packages except textual and textual_textarea
outdated_packages=$(pip list --outdated --format=columns | awk 'NR>2 {print $1}' | grep -Ev '^(textual|textual_textarea)$')
if [ -n "$outdated_packages" ]; then
    echo "Upgrading outdated packages (excluding textual and textual_textarea):"
    echo "$outdated_packages" | xargs -n1 pip install --upgrade
else
    echo "All packages are up to date (excluding textual and textual_textarea)."
<<<<<<< HEAD
fi
=======
fi

echo "Setup completed successfully."
>>>>>>> c470e6e651d04d481fcd7b060a6e16d7ec3c5d8f
