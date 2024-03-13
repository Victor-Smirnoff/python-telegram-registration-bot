@echo off

echo activate virtual environment venv

call %~dp0venv\Scripts\activate

echo virtual environment venv activated

echo run web app on FastAPI

start python web_app.py

echo run telegram bot

start python bot_app.py

echo two apps run

pause
