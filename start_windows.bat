@echo off

:: Create and activate virtual environment if it doesn't exist
if not exist "Otrace_venv" (
    python -m venv Otrace_venv

    :: Activate the virtual environment
    call Otrace_venv\Scripts\activate.bat

    :: Update pip to the latest version
    python.exe -m pip install --upgrade pip

    :: Install dependencies
    pip install bcrypt textual==0.89.1 textual_textarea==0.15.0 requests maskpass
)

:: Activate the virtual environment
call Otrace_venv\Scripts\activate.bat

:: Upgrade outdated packages if any
for /f "delims=" %%i in ('python -m pip list --outdated') do (
    for /f "tokens=1 delims==" %%j in ("%%i") do (
        echo Upgrading %%j
        python -m pip install --upgrade %%j || call :ErrorExit "Failed to upgrade some packages."
    )
)

echo Setup completed successfully.