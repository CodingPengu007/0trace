@echo off
setlocal EnableDelayedExpansion

REM Function to handle errors
:ERROR_EXIT
echo ERROR: %1 1>&2
exit /b 1

REM Create and activate virtual environment if it doesn't exist
if not exist "Otrace_venv\" (
    echo Creating virtual environment...
    python -m venv Otrace_venv || call :ERROR_EXIT "Failed to create virtual environment."
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
call Otrace_venv\Scripts\activate.bat || call :ERROR_EXIT "Failed to activate virtual environment."

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip || call :ERROR_EXIT "Failed to upgrade pip."

REM Install required packages
set required_packages=bcrypt textual==0.89.1 textual_textarea==0.15.0 requests maskpass

for %%p in (%required_packages%) do (
    if "%%p"=="readline" (
        echo Skipping installation of readline via pip. Ensure 'libreadline-dev' is installed on your system.
        goto :continue
    )
    echo Installing package: %%p...
    pip install %%p || call :ERROR_EXIT "Failed to install package: %%p."
    :continue
)

REM Upgrade outdated packages except textual and textual_textarea
echo Checking for outdated packages...
for /f "skip=2 tokens=1" %%o in ('pip list --outdated --format=columns') do (
    echo Upgrading outdated package: %%o...
    pip install --upgrade %%o || call :ERROR_EXIT "Failed to upgrade package: %%o."
)

echo Setup completed successfully.
exit /b 0