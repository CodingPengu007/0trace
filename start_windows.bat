@echo off
setlocal EnableDelayedExpansion

REM Function to handle errors
:ERROR_EXIT
echo %1 1>&2
exit /b 1

:MAIN
REM Create virtual environment if it doesn't exist
if not exist "Otrace_venv\" (
    python -m venv Otrace_venv || call :ERROR_EXIT "Failed to create virtual environment."
)

REM Activate the virtual environment
call Otrace_venv\Scripts\activate.bat || call :ERROR_EXIT "Failed to activate virtual environment."

REM Upgrade pip
pip install --upgrade pip
if errorlevel 1 call :ERROR_EXIT "Failed to upgrade pip."

REM Install required packages
set packages=bcrypt textual==0.89.1 textual_textarea==0.15.0 requests maskpass readline

for %%p in (%packages%) do (
    if "%%p"=="readline" (
        echo Skipping installation of readline via pip. Ensure any required system dependencies are installed.
    ) else (
        pip install %%p
        if errorlevel 1 call :ERROR_EXIT "Failed to install package: %%p."
    )
)

REM Upgrade outdated packages except textual and textual_textarea
for /f "skip=2 tokens=1" %%a in ('pip list --outdated --format=columns') do (
    echo %%a | findstr /i /v "textual" | findstr /i /v "textual_textarea" >nul
    if !errorlevel! == 0 (
        echo Upgrading package: %%a
        pip install --upgrade %%a
        if errorlevel 1 call :ERROR_EXIT "Failed to upgrade package: %%a."
    )
)

echo Setup completed successfully.
