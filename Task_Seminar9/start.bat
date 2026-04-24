@echo off
cd /d "%~dp0"
start "Server UDP" cmd /k "title Server UDP & py server.py"
timeout /t 1 /nobreak >nul
start "Client 1" cmd /k "title Client 1 & py client.py"
start "Client 2" cmd /k "title Client 2 & py client.py"
start "Client 3" cmd /k "title Client 3 & py client.py"
