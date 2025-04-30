@echo off

echo Avvio Riceiver...
cd RiceviDati
start cmd /k python main.py

cd..

echo Avvio Insert...
cd InserisciDati
start cmd /k python main.py
