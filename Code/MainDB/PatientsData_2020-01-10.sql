# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.4.10-MariaDB)
# Database: PatientsData
# Generation Time: 2020-01-10 16:27:58 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table data_sensors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `data_sensors`;

CREATE TABLE `data_sensors` (
  `pressure_id` varchar(50) NOT NULL DEFAULT '',
  `heart_id` varchar(50) NOT NULL,
  `glucose_id` varchar(50) NOT NULL DEFAULT '',
  `pressure_min` int(11) DEFAULT NULL,
  `pressure_max` int(11) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `glucose` int(11) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table info_patients
# ------------------------------------------------------------

DROP TABLE IF EXISTS `info_patients`;

CREATE TABLE `info_patients` (
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
  `time_stamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `info_patients` WRITE;
/*!40000 ALTER TABLE `info_patients` DISABLE KEYS */;

INSERT INTO `info_patients` (`id_patient`, `pressure_id`, `heart_id`, `glucose_id`, `name`, `surname`, `age`, `gender`, `height`, `weight`, `code`, `unit`, `time_stamp`)
VALUES
	('1','1','1','1','A','B','22','M','43','145',2,'Haha','2020-01-09 15:09:27'),
	('1','1','1','1','A','A','23','M','24','24',2,'Hsjaka','2020-01-09 15:15:49'),
	('1','1','1','1','A','A','22','M','171','77',3,'Haja','2020-01-09 15:28:57'),
	('1','2','2','2','A','A','22','M','181','80',2,'Ajaja','2020-01-09 15:31:58'),
	('1','3','3','3','A','@','21','H','134','789',2,'Haah','2020-01-09 15:34:10');

/*!40000 ALTER TABLE `info_patients` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
