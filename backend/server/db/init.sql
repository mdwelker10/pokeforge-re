-- Initialize the database

-- Tables with data to insert ---
CREATE TABLE IF NOT EXISTS `type` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(32) UNIQUE
);
delete from `type`; -- TODO remove this line when ready to deploy
INSERT INTO `type` (`name`) VALUES ('normal'), 
('fire'), ('water'), ('electric'), ('grass'), 
('ice'), ('fighting'), ('poison'), ('ground'), 
('flying'), ('psychic'), ('bug'), ('rock'), 
('ghost'), ('dragon'), ('dark'), ('steel'), 
('fairy'), ('stellar'), ('unknown');

CREATE TABLE IF NOT EXISTS `category` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(32) UNIQUE
);
delete from `category`; -- TODO remove this line when ready to deploy
INSERT INTO `category` (`name`) VALUES ('physical'), ('special'), ('status');

CREATE TABLE IF NOT EXISTS `nature` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(32) UNIQUE,
  `increasestat` VARCHAR(32) CHECK (`increasestat` IN ('hp', 'atk', 'def', 'spatk', 'spdef', 'spd')),
  `decreasestat` VARCHAR(32) CHECK (`decreasestat` IN ('hp', 'atk', 'def', 'spatk', 'spdef', 'spd'))
);
delete from `nature`; -- TODO remove this line when ready to deploy
INSERT INTO `nature` (`name`, `increasestat`, `decreasestat`) VALUES 
('hardy', 'atk', 'atk'), ('lonely', 'atk', 'def'), ('brave', 'atk', 'spd'), ('adamant', 'atk', 'spatk'), ('naughty', 'atk', 'spdef'), 
('bold', 'def', 'atk'), ('docile', 'def', 'def'), ('relaxed', 'def', 'spd'), ('impish', 'def', 'spatk'), ('lax', 'def', 'spdef'), 
('timid', 'spd', 'atk'), ('hasty', 'spd', 'def'), ('serious', 'spd', 'spd'), ('jolly', 'spd', 'spatk'), ('naive', 'spd', 'spdef'), 
('modest', 'spatk', 'atk'), ('mild', 'spatk', 'def'), ('quiet', 'spatk', 'spd'), ('bashful', 'spatk', 'spatk'), ('rash', 'spatk', 'spdef'), 
('calm', 'spdef', 'atk'), ('gentle', 'spdef', 'def'), ('sassy', 'spdef', 'spd'), ('careful', 'spdef', 'spatk'), ('quirky', 'spdef', 'spdef');

-- Tables that get populated as the app is used ---
-- Password/Salt can only be null if user is authenticating with google. Username becomes their email before the @ symbol
CREATE TABLE IF NOT EXISTS `user` (
  `id` INTEGER PRIMARY KEY,
  `username` VARCHAR(32) NOT NULL UNIQUE CHECK (LENGTH(`username`) > 2),
  `password` VARCHAR(256),
  `googleid` VARCHAR(256) UNIQUE,
  `email` VARCHAR(256) UNIQUE,
  `createdat` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `team` (
  `id` INTEGER PRIMARY KEY,
  `name` varchar(32) NOT NULL UNIQUE CHECK (LENGTH(`name`) > 2), 
  `public` BOOLEAN NOT NULL,
  `lastmodified` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- TODO add trigger to update this on update
  `generation` INTEGER NOT NULL DEFAULT 0, -- generation 0 means not generation specific (i.e. a showdown team or for fun)
  `userid` INTEGER NOT NULL,
  FOREIGN KEY (`userid`) REFERENCES `user`(`id`)
);

CREATE TABLE IF NOT EXISTS `move` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(32) NOT NULL,
  `mtypeid` INTEGER NOT NULL,
  `mcategoryid` INTEGER NOT NULL,
  FOREIGN KEY (`mtypeid`) REFERENCES `type`(`id`),
  FOREIGN KEY (`mcategoryid`) REFERENCES `category`(`id`)
);

CREATE TABLE IF NOT EXISTS `moveset` (
  `id` INTEGER PRIMARY KEY,
  `move1id` INTEGER NOT NULL,
  `move2id` INTEGER,
  `move3id` INTEGER,
  `move4id` INTEGER,
  FOREIGN KEY (`move1id`) REFERENCES `move`(`id`),
  FOREIGN KEY (`move2id`) REFERENCES `move`(`id`),
  FOREIGN KEY (`move3id`) REFERENCES `move`(`id`),
  FOREIGN KEY (`move4id`) REFERENCES `move`(`id`)
);

CREATE TABLE IF NOT EXISTS `pokemontypes` (
  `id` INTEGER PRIMARY KEY,
  `type1id` INTEGER NOT NULL,
  `type2id` INTEGER,
  `teratypeid` INTEGER,
  FOREIGN KEY (`type1id`) REFERENCES `type`(`id`),
  FOREIGN KEY (`type2id`) REFERENCES `type`(`id`),
  FOREIGN KEY (`teratypeid`) REFERENCES `type`(`id`)
);

CREATE TABLE IF NOT EXISTS `pokemon` (
  `id` INTEGER PRIMARY KEY,
  `name` VARCHAR(32) NOT NULL,
  `ability` VARCHAR(32),
  `shiny` BOOLEAN NOT NULL,
  `gender` VARCHAR(32) CHECK (`gender` IN ('male', 'female', 'genderless')) NOT NULL,
  `natureid` INTEGER,
  `movesetid` INTEGER NOT NULL,
  `pokemontypesid` INTEGER NOT NULL,
  `teamid` INTEGER NOT NULL,
  `form` VARCHAR(16),
  `evs` VARCHAR(64), --- JSON object with keys hp, atk, def, spatk, spdef, spd
  `ivs` VARCHAR(64), --- JSON object with keys hp, atk, def, spatk, spdef, spd
  FOREIGN KEY (`natureid`) REFERENCES `nature`(`id`),
  FOREIGN KEY (`movesetid`) REFERENCES `moveset`(`id`),
  FOREIGN KEY (`pokemontypesid`) REFERENCES `pokemontypes`(`id`),
  FOREIGN KEY (`teamid`) REFERENCES `team`(`id`)
);


