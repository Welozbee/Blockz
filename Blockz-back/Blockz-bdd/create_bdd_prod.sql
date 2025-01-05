DROP DATABASE IF EXISTS `blockz`;
CREATE DATABASE IF NOT EXISTS `blockz`;
USE `blockz`;
DROP TABLE IF EXISTS `blocks`;
CREATE TABLE IF NOT EXISTS `blocks` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL DEFAULT '0',
  `displayName` varchar(50) NOT NULL DEFAULT '0',
  `hardness` float NOT NULL DEFAULT (0),
  `resistance` float NOT NULL DEFAULT (0),
  `stackSize` int NOT NULL DEFAULT (0),
  `diggable` tinyint NOT NULL DEFAULT (0),
  `material` varchar(50) NOT NULL DEFAULT '0',
  `transparent` tinyint NOT NULL DEFAULT (0),
  `emitLight` int NOT NULL DEFAULT (0),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;