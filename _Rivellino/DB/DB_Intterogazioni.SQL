--Query ricerca percentuale batteria
	SELECT PercentualeBatteria
	FROM Scatola
	WHERE NomeScatola = '...';

--Query ricerca temperatura attuale
	SELECT Valore
	FROM Temperatura
	WHERE NameSensore = '...'
	ORDER BY Data DESC, Ora DESC
	LIMIT 1;

--Query ricerca umidita attuale
	SELECT Valore
	FROM Umidita
	WHERE NameSensore = '...'
	ORDER BY Data DESC, Ora DESC
	LIMIT 1;
	
--Query ricerca Co2 e No2 attuale
	SELECT ValoreCo, ValoreNo2
	FROM Qualita
	ORDER BY Data DESC, Ora DESC
	LIMIT 1;

--Query ricerca presenza di allagamento
	SELECT Valore
	FROM Allagamento
	ORDER BY Data DESC, Ora DESC
	LIMIT 1;

--Query ricerca dati vibrazione
	SELECT ValoreFrequenza, ValoreAmpiezza
	FROM Vibrazione
	ORDER BY Data DESC, Ora DESC
	LIMIT 1;