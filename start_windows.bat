@echo off

:: Function to print error messages and exit
:ErrorExit
echo %1 >&2
exit /b 1

:: Create and activate virtual environment if it doesn't exist
if not exist "Otrace_venv" (
    python -m venv Otrace_venv || call :ErrorExit "Failed to create virtual environment."
)

:: Activate the virtual environment
call Otrace_venv\Scripts\activate.bat || call :ErrorExit "Failed to activate virtual environment."

:: Install dependencies
python -m pip install --upgrade pip || call :ErrorExit "Failed to upgrade pip."
python -m pip install bcrypt texteditor requests || call :ErrorExit "Failed to install required packages."

:: Upgrade outdated packages if any
for /f "delims=" %%i in ('python -m pip list --outdated --format=freeze') do (
    for /f "tokens=1 delims==" %%j in ("%%i") do (
        echo Upgrading %%j
        python -m pip install --upgrade %%j || call :ErrorExit "Failed to upgrade some packages."
    )
)

echo Setup completed successfully.