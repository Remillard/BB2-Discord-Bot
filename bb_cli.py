#! python3
################################################################################
# Command line interface into the database
################################################################################
import os
import typer
from rich import print
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.table import Table

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
        if Confirm.ask(
            f"[bold red]Are you VERY sure you wish to delete {filename} and recreate?[/]",
            default=False,
        ):
            print("[bold red]Deleting specified database.[/]")
            os.remove(filename)
        else:
            raise typer.Abort()

    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.initialize_race_table(my_engine)
    print("[bold green]Completed setup of database.[/]")


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
    try:
        engine.add_team(my_engine, team_csv)
    except Exception as e:
        print(e)


################################################################################
# Find Coach Command
@cli.command("report_coaches")
def report_coaches(filename: str = "bb.db"):
    """
    Prints a table of the coaches table.
    """
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    rows = engine.get_all_coaches(my_engine)
    table = Table(title="Blood Bowl Coach List", safe_box=True, box=box.ROUNDED)
    table.add_column("Coach ID", justify="right", no_wrap=True)
    table.add_column("Discord", justify="right", no_wrap=True)
    table.add_column("BB2 Coach", justify="right", no_wrap=True)
    table.add_column("BB3 Coach", justify="right", no_wrap=True)
    for row in rows:
        table.add_row(str(row.id), row.d_name, row.bb2_name, row.bb3_name)
    console = Console()
    console.print(table)


@cli.command("report_teams")
def report_teams(filename: str = "bb.db"):
    """
    Prints a table of the teams table crossed with the coaches and races.
    """
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    rows = engine.get_all_teams(my_engine)
    table = Table(title="Blood Bowl Team List", safe_box=True, box=box.ROUNDED)
    table.add_column("Team ID", justify="right", no_wrap=True)
    table.add_column("Team Name", justify="right", no_wrap=True)
    table.add_column("Race", justify="right", no_wrap=True)
    table.add_column("BB Version", justify="right", no_wrap=True)
    table.add_column("Coach", justify="right", no_wrap=True)
    for row in rows:
        table.add_row(str(row[0]), row[1], row[2], str(row[3]), row[4])
    console = Console()
    console.print(table)


@cli.command("test_method")
def test_method(filename: str = "bb.db"):
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.get_all_teams(my_engine)


if __name__ == "__main__":
    cli()
