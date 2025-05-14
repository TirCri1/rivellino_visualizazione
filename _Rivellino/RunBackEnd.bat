@echo off

echo Avvio Riceiver...
start "Ricevi Dati" python BackEnd\RiceviDati\main.py

echo Avvio Insert...
start "Inserisci Dati" python BackEnd\InserisciDati\main.py
