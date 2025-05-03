@echo off
setlocal

:: Elimina il file vecchio, se esiste
del ipWindows.txt 2>nul

:: Ottiene l'indirizzo IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set ip=%%a
)

:: Rimuove eventuali spazi iniziali
set ip=%ip:~1%

:: stampa l'IP locale sul file
echo IP Locale: %ip% >> ipWindows.txt

echo -----------------------------------------------
echo   IP locale (%ip%) salvato in ipWindows.txt
echo -----------------------------------------------
echo     Premere un tasto per collegarsi all'ip
echo -----------------------------------------------
pause

:: Apre Chrome con una ricerca dell'indirizzo IP
start chrome "https://%ip%"