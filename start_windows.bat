@echo off

:: Function to print error messages and exit
:ErrorExit
echo %1 >&2
exit /b 1

:: Check if Git is installed, and install it if not
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed. Installing Git...
    powershell -Command "Start-Process 'https://git-scm.com/download/win' -Wait" || call :ErrorExit "Failed to install Git. Please install it manually."
)

:: Check if Python is installed, and install it if not
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -Wait" || call :ErrorExit "Failed to install Python. Please install it manually."
)

:: Check if python3 is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    call :ErrorExit "python3 could not be found. Please install Python 3."
)

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    call :ErrorExit "pip could not be found. Please install pip for Python 3."
)

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