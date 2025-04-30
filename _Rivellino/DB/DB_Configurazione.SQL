-- Tabella Scatola
INSERT INTO Scatola (NomeScatola, PercentualeBatteria) VALUES
('Scatola Muro', 100),
('Scatola Polveriera', 99),
('Scatola Galleria', 99);

-- Tabella Sensore
INSERT INTO Sensore (NameSensore, Tipo, NomeScatola) VALUES
('SensTemp1', 'Temperatura', 'Scatola Muro'),
('SensTemp2', 'Temperatura', 'Scatola Polveriera'),
('SensTemp3', 'Temperatura', 'Scatola Galleria'),
('SensUmid1', 'Umidità', 'Scatola Muro'),
('SensUmid2', 'Umidità', 'Scatola Polveriera'),
('SensUmid3', 'Umidità', 'Scatola Galleria'),
('SensQualitàAria', 'Qualità', 'Scatola Muro'),
('SensAllagamento', 'Allagamento', 'Scatola Galleria'),
('SensVibrazioni', 'Vibrazioni', 'Scatola Muro');
