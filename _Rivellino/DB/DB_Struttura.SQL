CREATE TABLE `Utente` (
    `userUtente` VARCHAR(20) UNIQUE NOT NULL,
	`paswordUtente` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`userUtente`)
);

CREATE TABLE `Scatola` (
    `NomeScatola` VARCHAR(20) UNIQUE NOT NULL,
	`PercentualeBatteria` INT,
    PRIMARY KEY (`NomeScatola`)
);

CREATE TABLE `Sensore` (
    `NameSensore` VARCHAR(20) UNIQUE NOT NULL,
    `Tipo` VARCHAR(15),
    `NomeScatola` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`NameSensore`),
    FOREIGN KEY (`NomeScatola`) REFERENCES `Scatola`(`NomeScatola`)
);

CREATE TABLE `Temperatura` (
    `Data` DATE NOT NULL,
    `Ora` TIME NOT NULL,
    `Valore` DOUBLE NOT NULL,
    `NameSensore` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Data`, `Ora`, `NameSensore`),
    FOREIGN KEY (`NameSensore`) REFERENCES `Sensore`(`NameSensore`)
);

CREATE TABLE `Umidita` (
    `Data` DATE NOT NULL,
    `Ora` TIME NOT NULL,
    `Valore` INT NOT NULL,
    `NameSensore` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Data`, `Ora`, `NameSensore`),
    FOREIGN KEY (`NameSensore`) REFERENCES `Sensore`(`NameSensore`)
);

CREATE TABLE `Qualita` (
    `Data` DATE NOT NULL,
    `Ora` TIME NOT NULL,
    `ValoreCo` DOUBLE NOT NULL,
	`ValoreNo2` DOUBLE NOT NULL,
    `NameSensore` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Data`, `Ora`, `NameSensore`),
    FOREIGN KEY (`NameSensore`) REFERENCES `Sensore`(`NameSensore`)
);

CREATE TABLE `Allagamento` (
    `Data` DATE NOT NULL,
    `Ora` TIME NOT NULL,
    `Valore` BOOLEAN NOT NULL,
    `NameSensore` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Data`, `Ora`, `NameSensore`),
    FOREIGN KEY (`NameSensore`) REFERENCES `Sensore`(`NameSensore`)
);

CREATE TABLE `Vibrazioni` (
    `Data` DATE NOT NULL,
    `Ora` TIME NOT NULL,
    `ValoreFrequenza` INT NOT NULL,
	`ValoreAmpiezza` INT NOT NULL,
    `NameSensore` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`Data`, `Ora`, `NameSensore`),
    FOREIGN KEY (`NameSensore`) REFERENCES `Sensore`(`NameSensore`)
);