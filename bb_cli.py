#! python3
################################################################################
# Command line interface into the database
################################################################################
import os
import typer

import models
import engine

################################################################################
# Main CLI interface entry point.
cli = typer.Typer()


@cli.command()
def initialize(filename: str):
    if os.path.exists(filename):
        answer = input(
            f"Are you VERY sure you wish to delete {filename} and recreate?  Type YES to continue, any other input to exit: "
        )
        if answer == "YES":
            print("Deleting specified database.")
            os.remove(filename)
        else:
            print("Exiting.")
            quit()

    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.initialize_race_table(my_engine)


@cli.command()
def add_coach(filename: str, coach_csv: str):
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.add_coach(my_engine, coach_csv)


if __name__ == "__main__":
    cli()
