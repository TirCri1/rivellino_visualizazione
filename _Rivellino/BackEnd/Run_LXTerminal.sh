#!/bin/bash

echo "Avvio Riceiver..."
cd RiceviDati || exit
lxterminal -e bash -c "python3 main.py; exec bash"
cd ..

echo "Avvio Insert..."
cd InserisciDati || exit
lxterminal -e bash -c "python3 main.py; exec bash"
