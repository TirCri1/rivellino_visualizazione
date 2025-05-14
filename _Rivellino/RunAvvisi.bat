@echo off

echo Avvio BOT...
start "BOT TELEGRAM" python Avvisi\BOT_Telegram\main.py

echo Avvio ALLERT...
start "CANALI TELEGRAM" python Avvisi\CANALE_Telegram\main.py
