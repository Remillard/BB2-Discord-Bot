CREATE TABLE `coaches` (
  `id` int PRIMARY KEY,
  `bb2_name` varchar(255),
  `discord_name` varchar(255),
  `discord_id` int
);

CREATE TABLE `teams` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `race` ENUM ('humans', 'orcs', 'dwarfs', 'skaven', 'dark_elves', 'brettonians', 'chaos', 'high_elves', 'wood_elves', 'undead', 'norse', 'necromantic', 'nurgle', 'lizardmen', 'pro_elves', 'mixed'),
  `coach_id` int
);

CREATE TABLE `tournaments` (
  `id` int PRIMARY KEY,
  `name` varchar(255),
  `state` ENUM ('open', 'in_progress', 'closed'),
  `num_teams` int,
  `num_rounds` int COMMENT 'index 1 to max',
  `current_round` int
);

CREATE TABLE `tournament_teams` (
  `id` int PRIMARY KEY,
  `tournament_id` int,
  `team` int
);

CREATE TABLE `games` (
  `id` int PRIMARY KEY,
  `tournament_id` int,
  `round_num` int COMMENT 'less than num_rounds',
  `home` int,
  `visitor` int,
  `state` ENUM ('unplayed', 'played', 'concession'),
  `home_score` int,
  `visitor_score` int
);

ALTER TABLE `teams` ADD FOREIGN KEY (`coach_id`) REFERENCES `coaches` (`id`);

ALTER TABLE `tournament_teams` ADD FOREIGN KEY (`tournament_id`) REFERENCES `tournaments` (`id`);

ALTER TABLE `tournament_teams` ADD FOREIGN KEY (`team`) REFERENCES `teams` (`id`);

ALTER TABLE `games` ADD FOREIGN KEY (`tournament_id`) REFERENCES `tournaments` (`id`);

ALTER TABLE `games` ADD FOREIGN KEY (`home`) REFERENCES `tournament_teams` (`id`);

ALTER TABLE `games` ADD FOREIGN KEY (`visitor`) REFERENCES `tournament_teams` (`id`);
