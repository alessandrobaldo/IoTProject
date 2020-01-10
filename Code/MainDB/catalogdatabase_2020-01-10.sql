# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.4.10-MariaDB)
# Database: catalogdatabase
# Generation Time: 2020-01-10 16:28:05 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table databases
# ------------------------------------------------------------

DROP TABLE IF EXISTS `databases`;

CREATE TABLE `databases` (
  `table` varchar(50) NOT NULL DEFAULT '',
  `attribute` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`table`,`attribute`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table mappings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mappings`;

CREATE TABLE `mappings` (
  `server` varchar(50) NOT NULL DEFAULT '',
  `ip` varchar(50) DEFAULT NULL,
  `port` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`server`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table mqtt
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mqtt`;

CREATE TABLE `mqtt` (
  `publisher` varchar(50) NOT NULL,
  `subscriber` varchar(50) DEFAULT '',
  `topic` varchar(50) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table sensors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sensors`;

CREATE TABLE `sensors` (
  `type` varchar(50) NOT NULL DEFAULT '',
  `id` int(11) NOT NULL,
  `available` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `sensors` WRITE;
/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;

INSERT INTO `sensors` (`type`, `id`, `available`)
VALUES
	('pressure',1,1),
	('pressure',2,1),
	('pressure',3,1),
	('pressure',4,1),
	('pressure',5,1),
	('pressure',6,1),
	('pressure',7,1),
	('pressure',8,1),
	('pressure',9,1),
	('pressure',10,1),
	('heart',1,1),
	('heart',2,1),
	('heart',3,1),
	('heart',4,1),
	('heart',5,1),
	('heart',6,1),
	('heart',7,1),
	('heart',8,1),
	('heart',9,1),
	('heart',10,1),
	('glucose',1,1),
	('glucose',2,1),
	('glucose',3,1),
	('glucose',4,1),
	('glucose',5,1),
	('glucose',6,1),
	('glucose',7,1),
	('glucose',8,1),
	('glucose',9,1),
	('glucose',10,1);

/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table telegram
# ------------------------------------------------------------

DROP TABLE IF EXISTS `telegram`;

CREATE TABLE `telegram` (
  `chat` varchar(50) DEFAULT NULL,
  `id` varchar(60) NOT NULL,
  `token` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table thresholds
# ------------------------------------------------------------

DROP TABLE IF EXISTS `thresholds`;

CREATE TABLE `thresholds` (
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

LOCK TABLES `thresholds` WRITE;
/*!40000 ALTER TABLE `thresholds` DISABLE KEYS */;

INSERT INTO `thresholds` (`person`, `minMinPres`, `maxMinPres`, `minAvgPres`, `maxAvgPres`, `minMaxPres`, `maxMaxPres`, `minGluc`, `maxGluc`)
VALUES
	('OVER65',83,121,86,134,91,147,60,130),
	('UNDER25',73,105,79,120,84,133,60,130),
	('UNDER45',77,110,82,123,87,137,60,130),
	('UNDER55',80,115,84,128,89,142,60,130),
	('UNDER65',82,118,86,132,91,142,60,130);

/*!40000 ALTER TABLE `thresholds` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
