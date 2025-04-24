@echo off

:: Create and activate virtual environment if it doesn't exist
if not exist "Otrace_venv" (
    python -m venv Otrace_venv
)

:: Activate the virtual environment
call Otrace_venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

echo Setup completed successfully.