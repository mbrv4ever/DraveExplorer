@echo off
REM ============================================================
REM  DraveExplorer - herstel: verwijdert en herbouwt de omgeving
REM ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

echo Dit verwijdert de map .venv en installeert alles opnieuw.
choice /c JN /n /m "Doorgaan? (J/N) "
if errorlevel 2 exit /b 0

if exist ".venv" (
    echo Oude omgeving verwijderen...
    rmdir /s /q ".venv"
)

set "PYEXE="
for %%V in (3.13 3.12 3.11 3.10) do (
    if not defined PYEXE (
        py -%%V -c "import sys" >nul 2>&1 && set "PYEXE=py -%%V"
    )
)
if not defined PYEXE (
    python --version >nul 2>&1 && set "PYEXE=python"
)
if not defined PYEXE (
    echo Geen geschikte Python gevonden.
    pause
    exit /b 1
)

%PYEXE% -m venv ".venv"
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
echo.
echo Klaar. Start het programma met run.bat
pause
