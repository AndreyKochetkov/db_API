CREATE DATABASE `forum_db` CHARACTER SET utf8 COLLATE utf8_general_ci;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `about` text,
  `isAnonymous` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`email`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#`name` varchar(255) DEFAULT NULL,

DROP TABLE IF EXISTS `forum`;

CREATE TABLE `forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `short_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL UNIQUE,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`short_name`),
  UNIQUE KEY `short_name_UNIQUE` (`short_name`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_forum_user_idx` (`user`),
  CONSTRAINT `fk_forum_user` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE NO ACTION ON UPDATE CASCADE
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `follow`;

CREATE TABLE `follow` (
  `follower` varchar(255) NOT NULL,
  `following` varchar(255) NOT NULL,
  UNIQUE KEY `uk_pair` (`follower`,`following`),
  CONSTRAINT `fk_follow_follower` FOREIGN KEY (`follower`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_follow_following` FOREIGN KEY (`following`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




DROP TABLE IF EXISTS `thread`;

CREATE TABLE `thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `message` text,
  `date` datetime DEFAULT NULL,
  `posts` int(11) NOT NULL DEFAULT '0',
  `likes` int(11) NOT NULL DEFAULT '0',
  `dislikes` int NOT NULL DEFAULT '0',
  `points` int(11) NOT NULL DEFAULT '0',
  `isClosed` tinyint(4) NOT NULL DEFAULT '0',
  `isDeleted` tinyint(4) NOT NULL DEFAULT '0',
  `forum` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_thread_forum_idx` (`forum`),
  KEY `fk_thread_user_idx` (`user`),
  CONSTRAINT `fk_thread_forum` FOREIGN KEY (`forum`) REFERENCES `forum` (`short_name`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `fk_thread_user` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




DROP TABLE IF EXISTS `subscribe`;

CREATE TABLE `subscribe` (
  `user` varchar(255) NOT NULL,
  `thread` int(11) NOT NULL,
  UNIQUE KEY `uk_pair` (`user`,`thread`),
  KEY `fk_subscribe_user_idx` (`user`),
  KEY `fk_subscribe_thread_idx` (`thread`),
  CONSTRAINT `fk_subscribe_thread` FOREIGN KEY (`thread`) REFERENCES `thread` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_subscribe_user` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `post`;

CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` text,
  `date` datetime DEFAULT NULL,
  `likes` int(11) DEFAULT '0',
  `dislikes` int(11) DEFAULT '0',
  `points` int(11) DEFAULT '0',
  `isApproved` tinyint(4) DEFAULT '0',
  `isHighlighted` tinyint(4) DEFAULT '0',
  `isEdited` tinyint(4) DEFAULT '0',
  `isSpam` tinyint(4) DEFAULT '0',
  `isDeleted` tinyint(4) DEFAULT '0',
  `forum` varchar(255) NOT NULL,
  `thread` int(11) NOT NULL,
  `user` varchar(255) NOT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `parent` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_post_forum_idx` (`forum`),
  KEY `fk_post_thread_idx` (`thread`),
  KEY `fk_post_user_idx` (`user`),
  CONSTRAINT `fk_post_forum` FOREIGN KEY (`forum`) REFERENCES `forum` (`short_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_post_thread` FOREIGN KEY (`thread`) REFERENCES `thread` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_post_user` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE NO ACTION ON UPDATE CASCADE
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
