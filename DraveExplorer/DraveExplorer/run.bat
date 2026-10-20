@echo off
REM ============================================================
REM  DraveExplorer - starten (zelfherstellend)
REM ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

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
    echo.
    echo Geen geschikte Python gevonden ^(3.10 t/m 3.13^).
    echo Installeer Python via https://www.python.org/downloads/
    echo en vink "Add Python to PATH" aan.
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" goto setup
goto start

:setup
echo.
echo Eenmalige installatie, even geduld...
%PYEXE% -m venv ".venv"
if errorlevel 1 goto venv_fout
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install --only-binary=:all: -r requirements.txt
if errorlevel 1 goto pip_fout
goto start

:start
call ".venv\Scripts\activate.bat"
start "" ".venv\Scripts\pythonw.exe" app.py
exit /b 0

:venv_fout
echo.
echo Kon de virtuele omgeving niet aanmaken.
echo Probeer herstel.bat of voer start-debug.bat uit voor details.
pause
exit /b 1

:pip_fout
echo.
echo Installatie van de pakketten is mislukt.
echo Controleer je internetverbinding en probeer herstel.bat.
pause
exit /b 1
