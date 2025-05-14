@echo off

echo Avvio BOT...
cd BOT_Telegram
start cmd /k python main.py

cd..

echo Avvio ALLERT...
cd CANALE_Telegram
start cmd /k python main.py
