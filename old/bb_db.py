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
        """
        Initialize a DBFile object with a connection.

        :param str filename: The filename of the database to connect to.
        """
        self.filename = filename
        try:
            self.conn = sqlite3.connect(self.filename)
        except Error as e:
            print(e)
        with self.conn:
            print(f"Connection to {self.filename} created.")

    def exec_sql(self, sql_cmd, sql_val=None):
        """
        Executes the SQL command passed to the method.

        :param str sql_cmd: The SQL command to be executed as a string.
        :param sql_val: The values associated with the SQL command.
        :type sql_val: tuple or None
        :return: Returns the list result of fetchall() against the command.  This list may be empty.
        """
        try:
            with self.conn:
                if sql_val is not None:
                    c = self.conn.execute(sql_cmd, sql_val)
                else:
                    c = self.conn.execute(sql_cmd)
                return c.fetchall()
        except Error as e:
            print(e)
        self.conn.commit()

    def init_tables(self):
        """
        Initializes a brand new database with the desired tables as described
        in the sql_strings module.
        """
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
        """
        Initializes new tables with table data that is intended to be used as
        enumerated types (which SQLite doesn't have.)
        """
        print("Filling enumerated state tables.")

        sqlcmd = sqlstr.insert_gamestate_cmd
        try:
            with self.conn:
                self.conn.executemany(sqlcmd, sqlstr.initial_gamestate_table)
        except Error as e:
            print(e)

        sqlcmd = sqlstr.insert_race_cmd
        try:
            with self.conn:
                self.conn.executemany(sqlcmd, sqlstr.initial_race_table)
        except Error as e:
            print(e)

        sqlcmd = sqlstr.insert_tourneystate_cmd
        try:
            with self.conn:
                self.conn.executemany(sqlcmd, sqlstr.initial_tourneystate_table)
        except Error as e:
            print(e)

        self.conn.commit()


################################################################################
class DBTable:
    """
    Abstract class for a SQLite3 table for common functionality.
    """

    def __init__(self, db_file):
        self.db_file = db_file


################################################################################
def main():
    """
    Main command line entry point.
    """
    parser = argparse.ArgumentParser(
        prog="bb_db",
        description="Methods to create a Blood Bowl tournament database.",
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
