import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from Funzioni import *

# Configurazione dell'email
mittente = "tiranti1cristian@gmail.com"
destinatario = "lorenzomuzzachi@gmail.com"
oggetto = "Report mesile dati Rivellino"
contenuto = f"Dati del mese: "
file = 'Avvisi/ReportEmail/report.pdf'

# Creazione del messaggio in formato corretto
messaggio = MIMEMultipart()
messaggio["From"] = mittente
messaggio["To"] = destinatario
messaggio["Subject"] = oggetto
messaggio.attach(MIMEText(contenuto, "plain"))


try:
    # Connessione al server SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()  # Saluto al server
    server.starttls()  # Avvio della connessione sicura
   
    # Login - Nota: è necessario utilizzare una password per app
    password_app = "dkfp phwc bspb mjzk"  # Sostituisci con la tua password per app
    server.login(mittente, password_app)
   
    # Invio dell'email
    testo_messaggio = messaggio.as_string()
    server.sendmail(mittente, destinatario, testo_messaggio)
    print("Email inviata con successo!")
   
    # Chiusura della connessione
    server.quit()
   
except Exception as e:
    print(f"Si è verificato un errore: {e}")
