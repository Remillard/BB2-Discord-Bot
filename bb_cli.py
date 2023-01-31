#! python3
################################################################################
# Command line interface into the database
################################################################################
import os
import argparse

import models
import engine

################################################################################
def main():
    """
    Main command line interface entry point.
    """
    parser = argparse.ArgumentParser(
        prog="bb_cli",
        description="An interface into the Blood Bowl tournament database.",
    )
    parser.add_argument("filename", help="The tournament SQLite3 database file.")
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="""Deletes the specified database if it exists and recreates the
        database initial state including enumerated tables.""",
    )
    parser.add_argument(
        "--add_coach",
        help='''Should have a parameter of a quoted string of a comma-separated
        list of values in the order: Discord Name, BB2 Coach Name, BB3 Coach Name.
        Example: "Remi#2160, Remillard, Remi"'''
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
    
        my_engine = engine.initialize_engine(args.filename)
        engine.initialize_tables(my_engine)
        engine.initialize_race_table(my_engine)
    else:
        my_engine = engine.initialize_engine(args.filename)
        engine.initialize_tables(my_engine)

    if args.add_coach:
        engine.add_coach(my_engine, args.add_coach)


if __name__ == "__main__":
    main()
