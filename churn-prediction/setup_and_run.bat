@echo off
setlocal
cd /d "%~dp0"
echo ============================================
echo CHURN PREDICTION - SETUP AND RUN LABS 3-10
echo ============================================
if not exist .venv (
    py -3.11 -m venv .venv
    if errorlevel 1 goto error
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if errorlevel 1 goto error
python -m pip install -r requirements.txt
if errorlevel 1 goto error
python download_dataset.py
if errorlevel 1 goto error
python run_all_labs.py
if errorlevel 1 goto error
echo.
echo ALL LABS COMPLETED SUCCESSFULLY.
pause
exit /b 0
:error
echo.
echo SETUP OR PIPELINE FAILED. Read the error above.
pause
exit /b 1
