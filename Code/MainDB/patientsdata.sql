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


-- Dump della struttura del database patientsdata
CREATE DATABASE IF NOT EXISTS `patientsdata` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `patientsdata`;

-- Dump della struttura di tabella patientsdata.data_sensors
CREATE TABLE IF NOT EXISTS `data_sensors` (
  `pressure_id` varchar(50) NOT NULL DEFAULT '',
  `heart_id` varchar(50) NOT NULL,
  `glucose_id` varchar(50) NOT NULL DEFAULT '',
  `pressure_min` int(11) DEFAULT NULL,
  `pressure_max` int(11) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `glucose` int(11) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella patientsdata.data_sensors: ~0 rows (circa)
/*!40000 ALTER TABLE `data_sensors` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_sensors` ENABLE KEYS */;

-- Dump della struttura di tabella patientsdata.info_patients
CREATE TABLE IF NOT EXISTS `info_patients` (
  `id_patient` varchar(50) NOT NULL,
  `pressure_id` varchar(50) NOT NULL,
  `heart_id` varchar(50) NOT NULL DEFAULT '',
  `glucose_id` varchar(50) NOT NULL DEFAULT '',
  `name` varchar(50) DEFAULT NULL,
  `surname` varchar(50) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `gender` varchar(50) DEFAULT NULL,
  `height` varchar(11) DEFAULT NULL,
  `weight` varchar(11) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT NULL,
  `processed` int(1) DEFAULT NULL,
  `analysed` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dump dei dati della tabella patientsdata.info_patients: ~3 rows (circa)
/*!40000 ALTER TABLE `info_patients` DISABLE KEYS */;
INSERT IGNORE INTO `info_patients` (`id_patient`, `pressure_id`, `heart_id`, `glucose_id`, `name`, `surname`, `age`, `gender`, `height`, `weight`, `code`, `unit`, `time_stamp`, `processed`, `analysed`) VALUES
	('1', '1', '1', '1', 'A', 'B', '22', 'M', '178', '67', 2, 'C', '2020-03-09 17:17:37', 0, 1),
	('2', '2', '2', '2', 'A', 'C', '55', 'M', '186', '76', 2, 'C', '2020-03-09 17:22:46', 0, 1),
	('3', '3', '3', '3', 'C', 'F', '65', 'M', '176', '67', 4, 'C', '2020-03-09 17:23:44', 0, 1),
	('4', '4', '4', '4', 'D', 'D', '67', 'F', '189', '87', 5, 'D', '2020-03-10 09:23:44', 0, 1),
	('5', '5', '5', '5', 'E', 'E', '32', 'O', '176', '120', 3, 'F', '2020-03-10 09:27:44', 0, 1),
	('6', '6', '6', '6', 'F', 'F', '45', 'F', '165', '87', 3, 'A', '2020-03-09 10:23:44', 0, 1),
	('7', '7', '7', '7', 'G', 'G', '12', 'M', '148', '65', 4, 'B', '2020-03-09 10:23:44', 0, 1),
	('8', '8', '8', '8', 'H', 'H', '89', 'F', '158', '89', 4, 'D', '2020-03-09 10:25:44', 0, 1),
	('9', '9', '9', '9', 'I', 'I', '37', 'F', '171', '74', 5, 'E', '2020-03-09 10:11:44', 0, 1),
	('1', '1', '1', '1', 'A', 'B', '34', 'M', '98', '78', 2, 'C', '2020-03-10 18:08:13', 0, 1),
	('2', '2', '2', '2', 'C', 'D', '67', 'F', '178', '78', 4, 'A', '2020-03-10 18:08:33', 0, 1);
/*!40000 ALTER TABLE `info_patients` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
