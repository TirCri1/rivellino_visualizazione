#!/bin/bash

# Elimina il file vecchio, se esiste
rm -f ipLinux.txt

# Ottiene l'indirizzo IP locale (escludendo loopback e interfacce virtuali)
ip=$(hostname -I | awk '{print $1}')

# Stampa l'IP locale nel file
echo "IP Locale: $ip" >> ipLinux.txt

echo "-----------------------------------------------"
echo "  IP locale ($ip) salvato in ip.txt"
echo "-----------------------------------------------"
read -p "     Premi Invio per collegarti all'IP..."
echo "-----------------------------------------------"

# Apre il browser predefinito all'indirizzo IP
xdg-open "http://$ip" &> /dev/null
