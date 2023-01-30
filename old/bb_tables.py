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
        """
        :param str bb_name: The in-game name of the Blood Bowl coach.
        :param str d_name: The Discord name of the coach in name#number format.
        """
        self.bb_name = bb_name
        self.d_name = d_name.split("#")[0]
        self.d_num = d_name.split("#")[1]

    @classmethod
    def from_str(cls, coach_str):
        """
        Receives a string containing comma separated values of the in-game
        coach name and the Discord user name.  Splits the string and returns a
        Coach object.

        :classmethod:
        :param str coach_str: The coach information in a CSV string, containing an in-game name and Discord name.
        :return: Returns an object of the Coach class.
        :rtype: Coach()
        """
        coach_list = coach_str.split(",")
        return cls(coach_list[0].lstrip(), coach_list[1].lstrip())

    @classmethod
    def from_record(cls, record):
        """
        Receives a tuple containing the objects retrieved from a SQL query
        against the coach table.  Produces a Coach object.

        :classmethod:
        :param record: The tuple from a SQL query.
        :rtype: Coach()
        """
        return cls(record[1], f"{record[2]}#{record[3]}")

    def __str__(self):
        """
        String method automatically called when Python decides to try
        to resolve the object as a string (for instance when used with print().)

        :return str: Returns the class object presented as a string.
        """
        return f"{self.bb_name}, {self.d_name}#{self.d_num}"


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

    def get_coach_by_id(self, id):
        """
        This method retrieves a coach record by selecting by the id field.

        :param int id: The table id field representing the row to be retrieved.
        :return: Returns a Coach object with the data from the record.
        :rtype: Coach()
        """
        sqlcmd = sqlstr.get_coach_by_id_cmd
        sqlval = (id,)
        coach_list = self.db_file.exec_sql(sqlcmd, sqlval)
        if coach_list:
            # This is SUPPOSED to be a single object in this context, however
            # there's no guarantee because exec_sql uses fetchall().  So
            # in this method explicitly calling out the initial list record.
            return Coach.from_record(coach_list[0])
        else:
            return None

    def del_coach_by_id(self, id):
        """
        This method removes a coach record by selecting by the id field.

        :param int id: The table id field representing the row to be deleted.
        """
        sqlcmd = sqlstr.delete_coach_by_id_cmd
        sqlval = (id,)
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
    parser.add_argument(
        "--del_coach_by_id", help="""Deletes a coach record given the row id."""
    )
    parser.add_argument(
        "--get_coach_by_id", help="""Prints out a coach record given the row id."""
    )
    args = parser.parse_args()

    # Make conneciton to the database
    db_file = DBFile(args.filename)

    if args.add_coach:
        Coaches(db_file).add_coach(Coach.from_str(args.add_coach))
    if args.del_coach_by_id:
        Coaches(db_file).del_coach_by_id(int(args.del_coach_by_id))
    if args.get_coach_by_id:
        coach = Coaches(db_file).get_coach_by_id(int(args.get_coach_by_id))
        if coach is not None:
            print(coach)
        else:
            print("There is no coach with that id.")


if __name__ == "__main__":
    main()
