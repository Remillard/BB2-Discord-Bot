#! python3
################################################################################
#
# Module of defined strings for SQL commands
#
create_coaches_table = """CREATE TABLE IF NOT EXISTS coaches (
    id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    bb2_name     TEXT NOT NULL,
    discord_name TEXT NOT NULL,
    discord_id   INTEGER NOT NULL
);"""

# Enumerated type for SQLite3
# Examples include:
#     * Human (BB2)
#     * Necromantic (BB2)
#     * Imperial Nobility (BB3)
#     * Necromantic Horror (BB3)
create_races_table = """CREATE TABLE IF NOT EXISTS races (
    id     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    race   TEXT NOT NULL,
    bb_ver INTEGER
);"""
initial_race_table = [
    ("Human", 2),
    ("Orc", 2),
    ("Dwarfs", 2),
    ("Skaven", 2),
    ("High Elves", 2),
    ("Dark Elves", 2),
    ("Bretonnians", 2),
    ("Chaos", 2),
    ("Wood Elves", 2),
    ("Lizardmen", 2),
    ("Norse", 2),
    ("Undead", 2),
    ("Necromantic", 2),
    ("Nurgle", 2),
    ("Chaos Dwarfs", 2),
    ("Khemri", 2),
    ("Halflings", 2),
    ("Ogres", 2),
    ("Goblins", 2),
    ("Vampires", 2),
    ("Amazon", 2),
    ("Elven Union", 2),
    ("Underworld", 2),
    ("Kislev Circus", 2),
    ("Black Orcs", 3),
    ("Chaos Chosen", 3),
    ("Chaos Renegades", 3),
    ("Dark Elves", 3),
    ("Dwarfs", 3),
    ("Elven Union", 3),
    ("Humans", 3),
    ("Imperial Nobility", 3),
    ("Nurgle", 3),
    ("Old World Alliance", 3),
    ("Orcs", 3),
    ("Skaven", 3),
]

create_teams_table = """CREATE TABLE IF NOT EXISTS teams (
    id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name     TEXT NOT NULL,
    bb_ver   INTEGER NOT NULL,
    race_id  INTEGER NOT NULL,
    coach_id INTEGER NOT NULL,
    FOREIGN KEY (coach_id) REFERENCES coaches (id),
    FOREIGN KEY (race_id)  REFERENCES races (id)
);"""

# Enumerated type for SQLite3
#    * Unplayed
#    * Played (to completion)
#    * Concession
create_tourneystates_table = """CREATE TABLE IF NOT EXISTS tourneystates (
    id    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    state TEXT NOT NULL
);"""
initial_tourneystate_table = [("Not Started",), ("In Progress",), ("Completed",)]

create_tournaments_table = """CREATE TABLE IF NOT EXISTS tournaments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name            TEXT NOT NULL,
    bb_ver          INTEGER NOT NULL,
    tourneystate_id TEXT NOT NULL,
    num_teams       INTEGER NOT NULL,
    num_rounds      INTEGER NOT NULL,
    current_round   INTEGER NOT NULL,
    FOREIGN KEY (tourneystate_id) REFERENCES tourneystates (id)
);"""

create_tournament_teams_table = """CREATE TABLE IF NOT EXISTS tournament_teams (
    id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tourney_id INTEGER NOT NULL,
    team_id    INTEGER NOT NULL,
    FOREIGN KEY (tourney_id) REFERENCES tournaments (id),
    FOREIGN KEY (team_id)    REFERENCES teams (id)
);"""

# Enumerated type for SQLite3
#    * Unplayed
#    * Played (to completion)
#    * Concession
create_gamestates_table = """CREATE TABLE IF NOT EXISTS gamestates (
    id    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    state TEXT NOT NULL
);"""
initial_gamestate_table = [("Unplayed",), ("Played",), ("Concession",)]

create_games_table = """CREATE TABLE IF NOT EXISTS games (
    id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tourney_id    INTEGER NOT NULL,
    round_num     INTEGER NOT NULL,
    home_id       INTEGER NOT NULL,
    visitor_id    INTEGER NOT NULL,
    gamestate_id  INTEGER NOT NULL,
    home_score    INTEGER,
    visitor_score INTEGER,
    FOREIGN KEY (tourney_id)   REFERENCES tournaments (id),
    FOREIGN KEY (home_id)      REFERENCES tournament_teams (id),
    FOREIGN KEY (visitor_id)   REFERENCES tournament_teams (id),
    FOREIGN KEY (gamestate_id) REFERENCES gamestate (id)
);"""
