@echo off
REM ============================================================
REM  DraveExplorer - bouw een losse .exe met PyInstaller
REM ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Voer eerst run.bat uit zodat de omgeving bestaat.
    pause
    exit /b 1
)
call ".venv\Scripts\activate.bat"

python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller installeren...
    pip install --only-binary=:all: pyinstaller
)

if not exist "app.ico" (
    echo Icoon aanmaken...
    python maak_icoon.py
)

echo.
echo Bouwen... dit kan even duren.
pyinstaller --noconfirm app.spec
echo.
echo Klaar. De .exe staat in de map "dist".
pause
