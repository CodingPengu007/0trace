@echo off
setlocal EnableDelayedExpansion

REM Function to handle errors
:ERROR_EXIT
echo %1 1>&2
exit /b 1

:MAIN
REM Create virtual environment if it doesn't exist
if not exist "Otrace_venv\" (
    python -m venv Otrace_venv
    if errorlevel 1 call :ERROR_EXIT "Failed to create virtual environment. Ensure Python is installed and added to PATH."
)

if exist "Otrace_venv\Scripts\activate.bat" (
    call Otrace_venv\Scripts\activate.bat || call :ERROR_EXIT "Failed to activate virtual environment."
) else (
    call :ERROR_EXIT "activate.bat not found. Ensure the virtual environment was created successfully."
)
call Otrace_venv\Scripts\activate.bat || call :ERROR_EXIT "Failed to activate virtual environment."

REM Upgrade pip
pip install --upgrade pip
if errorlevel 1 call :ERROR_EXIT "Failed to upgrade pip."

REM Install required packages
pip install bcrypt textual==0.89.1 textual_textarea==0.15.0 requests maskpass
if errorlevel 1 call :ERROR_EXIT "Failed to install required packages."