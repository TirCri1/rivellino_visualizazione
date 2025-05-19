
#Configurazioni


#Configurazioni del DB
DB_CONFIG = {
    #"host": "10.10.60.186",
    "host": "localhost",
    "user": "remoteUser",
    "password": "!rivellino!RIVELLINO!",
    "database": "rivellino"
}

TEMPERATURA = {
    "filePath": "BackEnd/DatiSensori/temperatura_umidita.csv",
    "fileStructure": ["timestamp", "modulo", "temperatura", "umidita"],
    "tabellaQuery": "temperatura",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": {
        "a": {"SensTemp1": "temperatura"},
        "b": {"SensTemp2": "temperatura"},
        "c": {"SensTemp3": "temperatura"}
    }
}

UMIDITA = {
    "filePath": "BackEnd/DatiSensori/temperatura_umidita.csv",
    "fileStructure": ["timestamp", "modulo", "temperatura", "umidita"],
    "tabellaQuery": "umidita",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": {
        "a": {"SensUmid1": "umidita"},
        "b": {"SensUmid2": "umidita"},
        "c": {"SensUmid3": "umidita"}
    }
}

QUALITA_ARIA_CO = {
    "filePath": "BackEnd/DatiSensori/ariaCO.csv",
    "fileStructure": ["timestamp", "modulo", "CO"],
    "tabellaQuery": "qualita",
    "dbStructure": ["Data", "Ora", "ValoreCo", "ValoreNo2", "NameSensore"],
    "sensori": {
        "a": {"SensQualitàAria1": {"ValoreCo": "CO"}}
    }
}

QUALITA_ARIA_NO2 = {
    "filePath": "BackEnd/DatiSensori/ariaNO2.csv",
    "fileStructure": ["timestamp", "modulo", "NO2"],
    "tabellaQuery": "qualita",
    "dbStructure": ["Data", "Ora", "ValoreCo", "ValoreNo2", "NameSensore"],
    "sensori": {
        "b": {"SensQualitàAria2": {"ValoreNo2": "NO2"}}
    }
}

VIBRAZIONE = {
    "filePath": "BackEnd/DatiSensori/vibrazioni.csv",
    "fileStructure": ["timestamp", "modulo", "vibrazione", "frequenza"],
    "tabellaQuery": "vibrazione",
    "dbStructure": ["Data", "Ora", "ValoreFrequenza", "ValoreAmpiezza", "NameSensore"],
    "sensori": {
        "a": {"SensVibrazione": {"frequenza": "ValoreFrequenza", "vibrazione": "ValoreAmpiezza"}}
    }
}

ALLAGAMENTO = {
    "filePath": "BackEnd/DatiSensori/allagamento.csv",
    "fileStructure": ["timestamp", "modulo", "allagamento"],
    "tabellaQuery": "allagamento",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": {
        "b": {"SensAllagamento": "allagamento"}
    }
}

ALIMENTAZIONE = {
    "filePath": "BackEnd/DatiSensori/batterie.csv",
    "fileStructure": ["timestamp", "modulo", "batteria"],
    "tabellaQuery": "scatola",
    "dbStructure": ["NomeScatola", "PercentualeBatteria"],
    "sensori": {
        "a": {"Scatola Muro": "batteria"},
        "b": {"Scatola Galleria": "batteria"},
        "c": {"Scatola Polveriera": "batteria"}
    }
}

STRUCTURE = {
    "temp": TEMPERATURA,
    "umid": UMIDITA,
    "ariaCO": QUALITA_ARIA_CO,
    "ariaNO2": QUALITA_ARIA_NO2,
    "vibrazione": VIBRAZIONE,
    "allagamento": ALLAGAMENTO,
    "alimentazione": ALIMENTAZIONE
}
