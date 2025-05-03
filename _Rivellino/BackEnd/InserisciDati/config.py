DB_CONFIG = {
    "host": "localhost",
    "user": "remoteUser",
    "password": "!rivellino!RIVELLINO!",
    "database": "rivellino"
}


TEMPERATURA =  {
    "path": "../RiceviDati/DatiSensori/temperatura_umidita.csv",
    "fileColoumn": ['timestamp', 'modulo', 'temperatura','umidita'],
    "query": "temperatura",
    "dbStructure" : ['Data', 'Ora', 'Valore', 'NameSensore'],
    "a": ["SensTemp1", "Valore", "temperatura"],
    "b": ["SensTemp2", "Valore", "temperatura"],
    "c": ["SensTemp3", "Valore", "temperatura"]
}
UMIDITA =  {
    "path": "../RiceviDati/DatiSensori/temperatura_umidita.csv",
    "fileColoumn": ['timestamp', 'modulo', 'temperatura','umidita'],
    "query": "umidita",
    "dbStructure" : ['Data', 'Ora', 'Valore', 'NameSensore'],
    "a": ["SensUmid1", "Valore", "umidita"],
    "b": ["SensUmid2", "Valore", "umidita"],
    "c": ["SensUmid3", "Valore", "umidita"]
}
QUALITA_ARIA =  {
    "path": "../RiceviDati/DatiSensori/aria.csv",
    "fileColoumn": ['timestamp', 'modulo', 'CO', 'NO2'],
    "query": "qualita",
    "dbStructure" : ['Data', 'Ora', 'ValoreCo', 'ValoreNo2', 'NameSensore'],
    "a": ["SensQualitàAria1", "ValoreCo", "CO"],
    "b": ["SensQualitàAria2", "ValoreNo2", "NO2"]
}
VIBRAZIONE =  {
    "path": "../RiceviDati/DatiSensori/vibrazioni.csv",
    "fileColoumn": ['timestamp', 'modulo', 'vibrazione','frequenza'],
    "query": "vibrazione",
    "dbStructure" : ['Data', 'Ora', 'ValoreFrequenza', 'ValoreAmpiezza', 'NameSensore'],
    "a": ["SensVibrazione", "ValoreFrequenza", "ValoreAmpiezza", "vibrazione", "frequenza"]
}
ALLAGAMENTO =  {
    "path": "../RiceviDati/DatiSensori/allagamento.csv",
    "fileColoumn": ['timestamp', 'modulo', 'allagamento'],
    "query": "allagamento",
    "dbStructure" : ['Data', 'Ora', 'Valore', 'NameSensore'],
    "b": ["SensAllagamento", "Valore", "allagamento"]
}

STRUCTURE = {
    "temp": TEMPERATURA,
    "umid": UMIDITA,
    "aria": QUALITA_ARIA,
    "vibrazione": VIBRAZIONE,
    "allagamento": ALLAGAMENTO,
}