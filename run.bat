@echo off
REM Start Django server in a new terminal
start cmd /k ".venv\Scripts\activate && python manage.py runserver"

REM Change directory to Angular frontend and start Angular in a new terminal
cd cart-frontend
start cmd /k "ng serve"