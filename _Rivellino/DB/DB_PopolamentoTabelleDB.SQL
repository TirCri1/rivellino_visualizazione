-- Popolamento della tabella Temperatura
INSERT INTO Temperatura (Data, Ora, Valore, NameSensore) VALUES
('2025-04-15', '08:30:00', 21.5, 'SensTemp1'),
('2025-04-15', '09:30:00', 21.0, 'SensTemp2'),
('2025-04-15', '12:00:00', 24.0, 'SensTemp1');

-- Popolamento della tabella Umidita
INSERT INTO Umidita (Data, Ora, Valore, NameSensore) VALUES
('2025-04-15', '08:00:00', 60, 'SensUmid1'),
('2025-04-15', '10:00:00', 70, 'SensUmid3'),
('2025-04-15', '14:00:00', 55, 'SensUmid1');

-- Popolamento della tabella Qualita
INSERT INTO Qualita (Data, Ora, ValoreCo2, ValoreNo2, NameSensore) VALUES
('2025-04-15', '06:00:00', 400.5, 40.2, 'SensQualitàAria'),
('2025-04-15', '09:00:00', 410.3, 39.8, 'SensQualitàAria');

-- Popolamento della tabella Allagamento
INSERT INTO Allagamento (Data, Ora, Valore, NameSensore) VALUES
('2025-04-15', '16:00:00', FALSE, 'SensAllagamento'),
('2025-04-15', '18:00:00', TRUE, 'SensAllagamento');

-- Popolamento della tabella Vibrazioni
INSERT INTO Vibrazioni (Data, Ora, ValoreFrequenza, ValoreAmpiezza, NameSensore) VALUES
('2025-04-15', '08:30:00', 15, 10, 'SensVibrazioni'),
('2025-04-15', '12:00:00', 20, 12, 'SensVibrazioni');
