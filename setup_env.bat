@echo off
setlocal

echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
set /p APP_NAME=Enter the app script name (default: app.py): 
if "%APP_NAME%"=="" set APP_NAME=app.py

if exist "%APP_NAME%" (
    echo Starting Streamlit app: %APP_NAME%
    streamlit run %APP_NAME%
) else (
    echo Error: The file %APP_NAME% does not exist.
)

pause
endlocal
