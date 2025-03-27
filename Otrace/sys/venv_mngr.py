#################################################################################

import sys
import os
import subprocess
import venv

#################################################################################

def create(main_dir, venv_dir):
    # Create a virtual environment
    venv.create(venv_dir, with_pip=True)

def activate(venv_dir):
    # Activate the virtual environment
    activate_script = os.path.join(venv_dir, 'Scripts', 'activate') if os.name == 'nt' else os.path.join(venv_dir, 'bin', 'activate')
    activate_command = f'source {activate_script}' if os.name != 'nt' else activate_script
    subprocess.call(activate_command, shell=True)

def install_bcrypt(venv_dir):
    # Install bcrypt in the virtual environment
    pip_executable = os.path.join(venv_dir, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_dir, 'Scripts', 'pip.exe')
    subprocess.call(f'{pip_executable} install bcrypt')
    
def setup(main_dir, venv_dir):
    # Create a virtual environment, activate it, and install bcrypt
    create(main_dir, venv_dir)
    activate(venv_dir)
    install_bcrypt(venv_dir)
    
def deactivate(venv_dir):
    # Deactivate the virtual environment
    deactivate_command = 'deactivate'
    subprocess.call(deactivate_command, shell=True)
    
def check(venv_dir):
    # Check if the virtual environment exists
    return os.path.exists(venv_dir)

#################################################################################