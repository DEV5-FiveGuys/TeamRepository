#!/bin/bash

# Django 서버 실행
echo "Starting Django server..."
cd Project1
python manage.py runserver &

# 서버가 시작될 시간을 기다림
sleep 3

# 브라우저 열기
echo "Opening browser..."
xdg-open http://127.0.0.1:8000/ 2>/dev/null || \
open http://127.0.0.1:8000/ || \
start http://127.0.0.1:8000/

# 서버 실행 중단 방지
wait
