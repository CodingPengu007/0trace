:: START SCRIPT
:: Windows

@echo off

:: Check if python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python could not be found. Please install Python 3.
    exit /b 1
)

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip could not be found. Please install pip for Python 3.
    exit /b 1
)

:: Create and activate virtual environment
python -m venv Otrace_venv
call Otrace_venv\Scripts\activate

:: Install dependencies
pip install bcrypt
pip install pyedit
pip install --upgrade pip
for /f "delims=" %%i in ('pip list --outdated --format=freeze ^| find "="') do pip install --upgrade %%i