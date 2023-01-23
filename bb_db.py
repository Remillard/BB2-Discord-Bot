#! python3
################################################################################
#
# Blood Bowl Bot Database Module
#
################################################################################
import os
import argparse

import sqlite3
from sqlite3 import Error

import sql_strings as sqlstr


################################################################################
def create_connection(db_file):
    db_conn = None
    try:
        db_conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return db_conn


################################################################################
def create_table(db_conn, sql_cmd):
    try:
        c = db_conn.cursor()
        c.execute(sql_cmd)
    except Error as e:
        print(e)


################################################################################
def init_tables(db_conn):
    # Enumerated Type Tables
    create_table(db_conn, sqlstr.create_races_table)
    create_table(db_conn, sqlstr.create_gamestates_table)
    create_table(db_conn, sqlstr.create_tourneystates_table)
    # Data Tables
    create_table(db_conn, sqlstr.create_coaches_table)
    create_table(db_conn, sqlstr.create_teams_table)
    create_table(db_conn, sqlstr.create_tournaments_table)
    create_table(db_conn, sqlstr.create_tournament_teams_table)
    create_table(db_conn, sqlstr.create_games_table)


################################################################################
def init_enum_tables(db_conn):
    sqlcmd = """INSERT INTO gamestates (state) VALUES (?)"""
    c = db_conn.cursor()
    for item in sqlstr.initial_gamestate_table:
        c.execute(sqlcmd, item)
    sqlcmd = """INSERT INTO races (race, bb_ver) VALUES (?, ?)"""
    for item in sqlstr.initial_race_table:
        c.execute(sqlcmd, item)
    sqlcmd = """INSERT INTO tourneystates (state) VALUES (?)"""
    for item in sqlstr.initial_tourneystate_table:
        c.execute(sqlcmd, item)
    db_conn.commit()


################################################################################
def add_coach(db_conn, coach):
    sqlcmd = (
        """INSERT INTO coaches (bb2_name, discord_name, discord_id) VALUES (?, ?, ?)"""
    )
    c = db_conn.cursor()
    c.execute(sqlcmd, coach)
    db_conn.commit()
    return c.lastrowid


################################################################################
def get_all_coaches(db_conn):
    c = db_conn.cursor()
    c.execute("select * from coaches")
    rows = c.fetchall()
    for row in rows:
        print(row)


################################################################################
def main():
    parser = argparse.ArgumentParser(
        prog="bb_db",
        description="Program to manipulate a Blood Bowl tournament database.",
    )
    parser.add_argument("filename", help="The tournament SQLite3 database file.")
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="""Deletes the specified database and recreates database initial state
        including enumerated state tables.""",
    )
    args = parser.parse_args()

    if args.initialize:
        answer = input(
            f"Are you VERY sure you wish to delete {args.filename} and recreate?  Type YES to continue, any other input to exit: "
        )
        if answer == "YES":
            if os.path.exists(args.filename):
                print("Deleting specified database.")
                os.remove(args.filename)
            db_conn = create_connection(args.filename)
            if db_conn is not None:
                print("Creating table structure.")
                init_tables(db_conn)
                print("Filling enumerated state tables.")
                init_enum_tables(db_conn)
            else:
                print("Error: DB connection handle invalid.")
        else:
            print("Exiting.")


if __name__ == "__main__":
    main()
