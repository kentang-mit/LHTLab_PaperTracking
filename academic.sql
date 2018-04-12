SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


CREATE TABLE `affiliation` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `article` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `title` varchar(1024) DEFAULT NULL,
  `url` text,
  `abstract` text,
  `conference` tinytext,
  `year` mediumint(8) UNSIGNED DEFAULT NULL,
  `month` tinyint(3) UNSIGNED DEFAULT NULL,
  `date` tinyint(3) UNSIGNED DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `author` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `affiliationid` mediumint(8) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `relationship` (
  `articleid` mediumint(8) UNSIGNED DEFAULT NULL,
  `authorid` mediumint(8) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE `affiliation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);


ALTER TABLE `article`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `title` (`title`);


ALTER TABLE `author`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `author_fk` (`affiliationid`);


ALTER TABLE `relationship`
  ADD KEY `rel_fk1` (`authorid`),
  ADD KEY `rel_fk2` (`articleid`);


ALTER TABLE `affiliation`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `article`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38393;

ALTER TABLE `author`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143506;

ALTER TABLE `author`
  ADD CONSTRAINT `author_fk` FOREIGN KEY (`affiliationid`) REFERENCES `affiliation` (`id`);

ALTER TABLE `relationship`
  ADD CONSTRAINT `rel_fk1` FOREIGN KEY (`authorid`) REFERENCES `author` (`id`),
  ADD CONSTRAINT `rel_fk2` FOREIGN KEY (`articleid`) REFERENCES `article` (`id`);