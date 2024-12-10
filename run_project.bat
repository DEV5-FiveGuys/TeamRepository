@echo off

REM Django 서버 실행
echo Starting Django server...
cd Project1
start cmd /k python manage.py runserver

REM 서버가 시작될 시간을 기다림
timeout /t 3 >nul

REM 브라우저 열기
echo Opening browser...
start http://127.0.0.1:8000/
