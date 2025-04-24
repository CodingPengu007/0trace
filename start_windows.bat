@echo off
setlocal EnableDelayedExpansion

REM Function to handle errors
:ERROR_EXIT
echo ERROR: %1 1>&2
exit /b 1

:MAIN
echo Starting script...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    call :ERROR_EXIT "Python is not installed or not added to PATH."
)

echo Python is installed.

REM Create virtual environment if it doesn't exist
if not exist "Otrace_venv\" (
    echo Creating virtual environment...
    python -m venv Otrace_venv
    if errorlevel 1 (
        call :ERROR_EXIT "Failed to create virtual environment."
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
echo Activating virtual environment...
call Otrace_venv\Scripts\activate.bat || call :ERROR_EXIT "Failed to activate virtual environment."

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip
if errorlevel 1 call :ERROR_EXIT "Failed to upgrade pip."

REM Install required packages
echo Installing required packages...
pip install bcrypt textual==0.89.1 textual_textarea==0.15.0 requests maskpass
if errorlevel 1 call :ERROR_EXIT "Failed to install required packages."

echo All tasks completed successfully.
exit /b 0