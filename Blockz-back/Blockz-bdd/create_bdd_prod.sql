DROP DATABASE IF EXISTS `blockz`;
CREATE DATABASE IF NOT EXISTS `blockz`;
USE `blockz`;
DROP TABLE IF EXISTS `blocks`;
DROP TABLE IF EXISTS `users`;
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
  `image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_users_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
