#! python3
################################################################################
#
# Module of defined strings for SQLite commands for the Blood Bowl database.
#
################################################################################
create_coaches_table = """CREATE TABLE IF NOT EXISTS coaches (
    id           INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    bb_name      TEXT NOT NULL,
    discord_name TEXT NOT NULL,
    discord_id   INTEGER NOT NULL
);"""
insert_coach_cmd = (
    """INSERT INTO coaches (bb_name, discord_name, discord_id) VALUES (?, ?, ?) """
)

# Enumerated type for SQLite3
# Examples include:
#     * Human (BB2)
#     * Necromantic (BB2)
#     * Imperial Nobility (BB3)
#     * Necromantic Horror (BB3)
create_races_table = """CREATE TABLE IF NOT EXISTS races (
    id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    race     TEXT NOT NULL,
    bb2_bool INTEGER NOT NULL,
    bb3_bool INTEGER NOT NULL
);"""
initial_race_table = [
    ("Humans", 1, 1),
    ("Orcs", 1, 1),
    ("Dwarfs", 1, 1),
    ("Skaven", 1, 1),
    ("Dark Elves", 1, 1),
    ("Nurgle", 1, 1),
    ("Elven Union", 1, 1),
    ("High Elves", 1, 0),
    ("Bretonnians", 1, 0),
    ("Chaos", 1, 0),
    ("Wood Elves", 1, 0),
    ("Lizardmen", 1, 0),
    ("Norse", 1, 0),
    ("Undead", 1, 0),
    ("Necromantic", 1, 0),
    ("Chaos Dwarfs", 1, 0),
    ("Khemri", 1, 0),
    ("Halflings", 1, 0),
    ("Ogres", 1, 0),
    ("Goblins", 1, 0),
    ("Vampires", 1, 0),
    ("Amazon", 1, 0),
    ("Underworld", 1, 0),
    ("Kislev Circus", 1, 0),
    ("Black Orcs", 0, 1),
    ("Chaos Chosen", 0, 1),
    ("Chaos Renegades", 0, 1),
    ("Imperial Nobility", 0, 1),
    ("Old World Alliance", 0, 1),
]
insert_race_cmd = """INSERT INTO races (race, bb2_bool, bb3_bool) VALUES (?, ?, ?)"""

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
insert_tourneystate_cmd = """INSERT INTO tourneystates (state) VALUES (?)"""

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
    bb_ver     INTEGER NOT NULL,
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
insert_gamestate_cmd = """INSERT INTO gamestates (state) VALUES (?)"""

create_games_table = """CREATE TABLE IF NOT EXISTS games (
    id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    bb_ver        INTEGER NOT NULL,
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
