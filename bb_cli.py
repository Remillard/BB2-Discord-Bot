#! python3
################################################################################
# Command line interface into the database
################################################################################
import os
import typer
from rich import print as rprint
from rich.console import Console

import models
import engine

################################################################################
# Main CLI interface entry point.
cli = typer.Typer()


################################################################################
# Initialization Command
@cli.command()
def initialize(filename: str = "bb.db"):
    """
    Initializes the database with tables and auto-filled static tables.  If the
    database already exists, a confirmation whether to delete the database and
    recreate must be answered.
    """
    if os.path.exists(filename):
        console = Console()
        answer = console.input(
            f"[bold red]Are you VERY sure you wish to delete {filename} and recreate?  Type YES to continue, any other input to exit:[/] "
        )
        if answer == "YES":
            rprint("[bold red]Deleting specified database.[/]")
            os.remove(filename)
        else:
            raise typer.Abort()

    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.initialize_race_table(my_engine)
    rprint("[bold green]Completed setup of database.[/]")


################################################################################
# Add Coach Command
@cli.command("add_coach")
def add_coach(coach_csv: str, filename: str = "bb.db"):
    """
    Command adds a coach record to the database.  The record should be
    a comma separated list as a quoted string.  The order of records is:
    "<Discord name>, <Blood Bowl 2 in-game name>, <Blood Bowl 3 in-game name>"
    """
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.add_coach(my_engine, coach_csv)


################################################################################
# Add Team Command
@cli.command("add_team")
def add_team(team_csv: str, filename: str = "bb.db"):
    """
    Command adds a team record to the database.  The record should be
    a comma separated list as a quoted string.  The order of records is:
    "<Discord name>, <Team Name>, <Race Name>"
    """
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.add_team(my_engine, team_csv)


################################################################################
# Find Coach Command
@cli.command("find_coach")
def find_coach(d_name: str, filename: str = "bb.db"):
    """
    Command adds a coach record to the database.  The record should be
    a comma separated list as a quoted string.  The order of records is:
    "<Discord name>, <Blood Bowl 2 in-game name>, <Blood Bowl 3 in-game name>"
    """
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.find_coach(my_engine, d_name)


if __name__ == "__main__":
    cli()
