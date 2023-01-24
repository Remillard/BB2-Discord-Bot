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
class DBFile:
    """Class encapsulating the SQLite database file and initialization."""

    def __init__(self, filename):
        self.filename = filename
        self.conn = self.create_connection()

    def create_connection(self):
        """Opens a connection with the database file the class instance is
        associated with."""
        conn = None
        try:
            conn = sqlite3.connect(self.filename)
        except Error as e:
            print(e)
        return conn

    def exec_sql(self, sql_cmd):
        """Executes the SQL command passed to the method."""
        try:
            c = self.conn.cursor()
            c.execute(sql_cmd)
        except Error as e:
            print(e)
        self.conn.commit()

    def init_tables(self):
        """Initializes a brand new database with the desired tables as described
        in the sql_strings module."""
        print("Creating table structure.")
        # Enumerated Type Tables
        self.exec_sql(sqlstr.create_races_table)
        self.exec_sql(sqlstr.create_gamestates_table)
        self.exec_sql(sqlstr.create_tourneystates_table)
        # Data Tables
        self.exec_sql(sqlstr.create_coaches_table)
        self.exec_sql(sqlstr.create_teams_table)
        self.exec_sql(sqlstr.create_tournaments_table)
        self.exec_sql(sqlstr.create_tournament_teams_table)
        self.exec_sql(sqlstr.create_games_table)

    def init_enum_tables(self):
        """Initializes new tables with table data that is intended to be used as
        enumerated types (which SQLite doesn't have.)"""
        print("Filling enumerated state tables.")
        c = self.conn.cursor()

        sqlcmd = sqlstr.insert_gamestate_cmd
        for item in sqlstr.initial_gamestate_table:
            c.execute(sqlcmd, item)

        sqlcmd = sqlstr.insert_race_cmd
        for item in sqlstr.initial_race_table:
            c.execute(sqlcmd, item)

        sqlcmd = sqlstr.insert_tourneystate_cmd
        for item in sqlstr.initial_tourneystate_table:
            c.execute(sqlcmd, item)

        self.conn.commit()


################################################################################
# def add_coach(db_conn, coach):
#     sqlcmd = sqlstr.insert_coach_cmd
#     c = db_conn.cursor()
#     c.execute(sqlcmd, coach)
#     db_conn.commit()
#     return c.lastrowid


################################################################################
# def get_all_coaches(db_conn):
#     c = db_conn.cursor()
#     c.execute("select * from coaches")
#     rows = c.fetchall()
#     for row in rows:
#         print(row)


################################################################################
def main():
    """Main command line entry point."""
    #
    # Command line arguments.
    #
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
        if os.path.exists(args.filename):
            answer = input(
                f"Are you VERY sure you wish to delete {args.filename} and recreate?  Type YES to continue, any other input to exit: "
            )
            if answer == "YES":
                print("Deleting specified database.")
                os.remove(args.filename)
            else:
                print("Exiting.")
                quit()
        db_file = DBFile(args.filename)
        db_file.init_tables()
        db_file.init_enum_tables()
        print(f"Database {args.filename} initialization complete!")


if __name__ == "__main__":
    main()
