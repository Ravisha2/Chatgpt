@echo off
REM Double-click this file to start the Wi-Fi speed test server.
title Simple Speed Test
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py server.py
) else (
  python server.py
)
echo.
echo The server has stopped. If you saw an error above, make sure Python is installed
echo with "Add python.exe to PATH" ticked.
pause
