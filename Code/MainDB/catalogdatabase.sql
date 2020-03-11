-- --------------------------------------------------------
-- Host:                         localhost
-- Versione server:              10.1.39-MariaDB - mariadb.org binary distribution
-- S.O. server:                  Win64
-- HeidiSQL Versione:            10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dump della struttura del database catalogdatabase
CREATE DATABASE IF NOT EXISTS `catalogdatabase` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `catalogdatabase`;

-- Dump della struttura di tabella catalogdatabase.databases
CREATE TABLE IF NOT EXISTS `databases` (
  `table` varchar(50) NOT NULL DEFAULT '',
  `attribute` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`table`,`attribute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.databases: ~0 rows (circa)
/*!40000 ALTER TABLE `databases` DISABLE KEYS */;
/*!40000 ALTER TABLE `databases` ENABLE KEYS */;

-- Dump della struttura di tabella catalogdatabase.mappings
CREATE TABLE IF NOT EXISTS `mappings` (
  `server` varchar(50) NOT NULL DEFAULT '',
  `ip` varchar(50) DEFAULT NULL,
  `port` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`server`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.mappings: ~0 rows (circa)
/*!40000 ALTER TABLE `mappings` DISABLE KEYS */;
/*!40000 ALTER TABLE `mappings` ENABLE KEYS */;

-- Dump della struttura di tabella catalogdatabase.mqtt
CREATE TABLE IF NOT EXISTS `mqtt` (
  `publisher` varchar(50) NOT NULL,
  `subscriber` varchar(50) DEFAULT '',
  `topic` varchar(50) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.mqtt: ~0 rows (circa)
/*!40000 ALTER TABLE `mqtt` DISABLE KEYS */;
/*!40000 ALTER TABLE `mqtt` ENABLE KEYS */;

-- Dump della struttura di tabella catalogdatabase.sensors
CREATE TABLE IF NOT EXISTS `sensors` (
  `type` varchar(50) NOT NULL DEFAULT '',
  `id` int(11) NOT NULL,
  `available` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.sensors: ~30 rows (circa)
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;
INSERT IGNORE INTO `sensors` (`type`, `id`, `available`) VALUES
	('pressure', 1, 1),
	('pressure', 2, 1),
	('pressure', 3, 1),
	('pressure', 4, 1),
	('pressure', 5, 1),
	('pressure', 6, 1),
	('pressure', 7, 1),
	('pressure', 8, 1),
	('pressure', 9, 1),
	('pressure', 10, 1),
	('heart', 1, 1),
	('heart', 2, 1),
	('heart', 3, 1),
	('heart', 4, 1),
	('heart', 5, 1),
	('heart', 6, 1),
	('heart', 7, 1),
	('heart', 8, 1),
	('heart', 9, 1),
	('heart', 10, 1),
	('glucose', 1, 1),
	('glucose', 2, 1),
	('glucose', 3, 1),
	('glucose', 4, 1),
	('glucose', 5, 1),
	('glucose', 6, 1),
	('glucose', 7, 1),
	('glucose', 8, 1),
	('glucose', 9, 1),
	('glucose', 10, 1);
/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;

-- Dump della struttura di tabella catalogdatabase.telegram
CREATE TABLE IF NOT EXISTS `telegram` (
  `chat` varchar(50) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `token` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.telegram: ~0 rows (circa)
/*!40000 ALTER TABLE `telegram` DISABLE KEYS */;
/*!40000 ALTER TABLE `telegram` ENABLE KEYS */;

-- Dump della struttura di tabella catalogdatabase.thresholds
CREATE TABLE IF NOT EXISTS `thresholds` (
  `person` varchar(50) NOT NULL DEFAULT '',
  `minMinPres` int(11) DEFAULT NULL,
  `maxMinPres` int(11) DEFAULT NULL,
  `minAvgPres` int(11) DEFAULT NULL,
  `maxAvgPres` int(11) DEFAULT NULL,
  `minMaxPres` int(11) DEFAULT NULL,
  `maxMaxPres` int(11) DEFAULT NULL,
  `minGluc` int(11) DEFAULT NULL,
  `maxGluc` int(11) DEFAULT NULL,
  PRIMARY KEY (`person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella catalogdatabase.thresholds: ~5 rows (circa)
/*!40000 ALTER TABLE `thresholds` DISABLE KEYS */;
INSERT IGNORE INTO `thresholds` (`person`, `minMinPres`, `maxMinPres`, `minAvgPres`, `maxAvgPres`, `minMaxPres`, `maxMaxPres`, `minGluc`, `maxGluc`) VALUES
	('OVER65', 83, 121, 86, 134, 91, 147, 60, 130),
	('UNDER25', 73, 105, 79, 120, 84, 133, 60, 130),
	('UNDER45', 77, 110, 82, 123, 87, 137, 60, 130),
	('UNDER55', 80, 115, 84, 128, 89, 142, 60, 130),
	('UNDER65', 82, 118, 86, 132, 91, 142, 60, 130);
/*!40000 ALTER TABLE `thresholds` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
