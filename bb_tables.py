#!python3
################################################################################
#
# Blood Bowl Bot Table Models
#
################################################################################
import os
import argparse
import sqlite3
from sqlite3 import Error

from bb_db import DBFile
from bb_db import DBTable
import sql_strings as sqlstr

################################################################################
class Coach:
    """
    Class containing the attributes of a coach record and methods for
    extracting from various sources, and methods for rendering into various
    ways.
    """

    def __init__(self, bb_name, d_name):
        self.bb_name = bb_name
        self.d_name = d_name.split("#")[0]
        self.d_num = d_name.split("#")[1]

    @classmethod
    def from_str(cls, coach_str):
        """
        Receives a string containing comma separated values of the in-game
        coach name and the Discord user name.  Splits the string and returns a
        class object.

        :classmethod:
        :param str coach_str: The coach information in a CSV string, containing an in-game name and Discord name.
        :return: Returns an object of the Coach class.
        :rtype: Coach()
        """
        coach_list = coach_str.split(",")
        return cls(coach_list[0].lstrip(), coach_list[1].lstrip())


################################################################################
class Coaches(DBTable):
    """
    Model class for the Coaches table.  Inherits from the Table class in the
    bb_db module.
    """

    def __init__(self, db_file):
        super().__init__(db_file)
        self.sql_table = "coaches"

    def add_coach(self, coach):
        """
        The coach parameter is an instance of the Coach class that contains
        the values from the command line string, including the Blood Bowl
        in-game coach name, and the Discord name including the # identifier.

        :param coach: The coach information to be added to the database.
        :type coach: Coach()
        """
        sqlcmd = sqlstr.insert_coach_cmd
        sqlval = (coach.bb_name, coach.d_name, coach.d_num)
        print(f"Adding record for {sqlval[0]}, {sqlval[1]}, {sqlval[2]}.")
        self.db_file.exec_sql(sqlcmd, sqlval)


################################################################################
def main():
    """
    Main command line entry point.
    """
    parser = argparse.ArgumentParser(
        prog="bb_tables",
        description="Methods to manipulate the Blood Bowl tournament database.",
    )
    parser.add_argument("filename", help="The tournament SQLite3 database file.")
    parser.add_argument(
        "--add_coach",
        help='''Adds a coach to the coach table in the database.  Format should
        be a comma separated list inside quotes in the following order: "Blood
        Bowl Coach Name, DiscordName#DiscordNum".
        Example: --add_coach "JohnnyBravo, jeremy#1234"''',
    )
    args = parser.parse_args()

    # Make conneciton to the database
    db_file = DBFile(args.filename)

    if args.add_coach:
        Coaches(db_file).add_coach(Coach.from_str(args.add_coach))


if __name__ == "__main__":
    main()
