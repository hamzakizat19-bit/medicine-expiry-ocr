@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
"C:\Users\direc\AppData\Local\Programs\Python\Python312\python.exe" medicine_ocr.py medicine.jpg medicine_2.jpg medicine_3.jpg
pause
