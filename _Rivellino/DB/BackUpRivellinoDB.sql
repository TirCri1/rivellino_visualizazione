-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Mag 03, 2025 alle 19:41
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rivellino`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `allagamento`
--

CREATE TABLE `allagamento` (
  `Data` date NOT NULL,
  `Ora` time NOT NULL,
  `Valore` tinyint(1) DEFAULT 1,
  `NameSensore` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `qualita`
--

CREATE TABLE `qualita` (
  `Data` date NOT NULL,
  `Ora` time NOT NULL,
  `ValoreCo` double DEFAULT -1,
  `ValoreNo2` double DEFAULT -1,
  `NameSensore` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `scatola`
--

CREATE TABLE `scatola` (
  `NomeScatola` varchar(20) NOT NULL,
  `PercentualeBatteria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `scatola`
--

INSERT INTO `scatola` (`NomeScatola`, `PercentualeBatteria`) VALUES
('Scatola Galleria', 99),
('Scatola Muro', 100),
('Scatola Polveriera', 99);

-- --------------------------------------------------------

--
-- Struttura della tabella `sensore`
--

CREATE TABLE `sensore` (
  `NameSensore` varchar(20) NOT NULL,
  `Tipo` varchar(15) DEFAULT NULL,
  `NomeScatola` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `sensore`
--

INSERT INTO `sensore` (`NameSensore`, `Tipo`, `NomeScatola`) VALUES
('SensAllagamento', 'Allagamento', 'Scatola Galleria'),
('SensQualitàAria1', 'Qualità', 'Scatola Muro'),
('SensQualitàAria2', 'Qualità', 'Scatola Polveriera'),
('SensTemp1', 'Temperatura', 'Scatola Muro'),
('SensTemp2', 'Temperatura', 'Scatola Polveriera'),
('SensTemp3', 'Temperatura', 'Scatola Galleria'),
('SensUmid1', 'Umidità', 'Scatola Muro'),
('SensUmid2', 'Umidità', 'Scatola Polveriera'),
('SensUmid3', 'Umidità', 'Scatola Galleria'),
('SensVibrazione', 'Vibrazioni', 'Scatola Muro');

-- --------------------------------------------------------

--
-- Struttura della tabella `temperatura`
--

CREATE TABLE `temperatura` (
  `Data` date NOT NULL,
  `Ora` time NOT NULL,
  `Valore` double NOT NULL,
  `NameSensore` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `umidita`
--

CREATE TABLE `umidita` (
  `Data` date NOT NULL,
  `Ora` time NOT NULL,
  `Valore` int(11) NOT NULL,
  `NameSensore` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `utente`
--

CREATE TABLE `utente` (
  `userUtente` varchar(50) NOT NULL,
  `passwordUtente` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `utente`
--

INSERT INTO `utente` (`userUtente`, `passwordUtente`) VALUES
('admin', '$2y$10$gNqOAnU.JI/EP8EK4UFL0.vBwEBQsdRbaerf7jk4HRHTLzR68/mc.');

-- --------------------------------------------------------

--
-- Struttura della tabella `vibrazione`
--

CREATE TABLE `vibrazione` (
  `Data` date NOT NULL,
  `Ora` time NOT NULL,
  `ValoreFrequenza` int(11) NOT NULL,
  `ValoreAmpiezza` int(11) NOT NULL,
  `NameSensore` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `allagamento`
--
ALTER TABLE `allagamento`
  ADD PRIMARY KEY (`Data`,`Ora`,`NameSensore`),
  ADD KEY `NameSensore` (`NameSensore`);

--
-- Indici per le tabelle `qualita`
--
ALTER TABLE `qualita`
  ADD PRIMARY KEY (`Data`,`Ora`,`NameSensore`),
  ADD KEY `NameSensore` (`NameSensore`);

--
-- Indici per le tabelle `scatola`
--
ALTER TABLE `scatola`
  ADD PRIMARY KEY (`NomeScatola`),
  ADD UNIQUE KEY `NomeScatola` (`NomeScatola`);

--
-- Indici per le tabelle `sensore`
--
ALTER TABLE `sensore`
  ADD PRIMARY KEY (`NameSensore`),
  ADD UNIQUE KEY `NameSensore` (`NameSensore`),
  ADD KEY `NomeScatola` (`NomeScatola`);

--
-- Indici per le tabelle `temperatura`
--
ALTER TABLE `temperatura`
  ADD PRIMARY KEY (`Data`,`Ora`,`NameSensore`),
  ADD KEY `NameSensore` (`NameSensore`);

--
-- Indici per le tabelle `umidita`
--
ALTER TABLE `umidita`
  ADD PRIMARY KEY (`Data`,`Ora`,`NameSensore`),
  ADD KEY `NameSensore` (`NameSensore`);

--
-- Indici per le tabelle `utente`
--
ALTER TABLE `utente`
  ADD PRIMARY KEY (`userUtente`),
  ADD UNIQUE KEY `userUtente` (`userUtente`);

--
-- Indici per le tabelle `vibrazione`
--
ALTER TABLE `vibrazione`
  ADD PRIMARY KEY (`Data`,`Ora`,`NameSensore`),
  ADD KEY `NameSensore` (`NameSensore`);

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `allagamento`
--
ALTER TABLE `allagamento`
  ADD CONSTRAINT `allagamento_ibfk_1` FOREIGN KEY (`NameSensore`) REFERENCES `sensore` (`NameSensore`);

--
-- Limiti per la tabella `qualita`
--
ALTER TABLE `qualita`
  ADD CONSTRAINT `qualita_ibfk_1` FOREIGN KEY (`NameSensore`) REFERENCES `sensore` (`NameSensore`);

--
-- Limiti per la tabella `sensore`
--
ALTER TABLE `sensore`
  ADD CONSTRAINT `sensore_ibfk_1` FOREIGN KEY (`NomeScatola`) REFERENCES `scatola` (`NomeScatola`);

--
-- Limiti per la tabella `temperatura`
--
ALTER TABLE `temperatura`
  ADD CONSTRAINT `temperatura_ibfk_1` FOREIGN KEY (`NameSensore`) REFERENCES `sensore` (`NameSensore`);

--
-- Limiti per la tabella `umidita`
--
ALTER TABLE `umidita`
  ADD CONSTRAINT `umidita_ibfk_1` FOREIGN KEY (`NameSensore`) REFERENCES `sensore` (`NameSensore`);

--
-- Limiti per la tabella `vibrazione`
--
ALTER TABLE `vibrazione`
  ADD CONSTRAINT `vibrazione_ibfk_1` FOREIGN KEY (`NameSensore`) REFERENCES `sensore` (`NameSensore`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
