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


@cli.command()
def initialize(filename: str = "bb.db"):
    '''
    Initializes the database with tables and auto-filled static tables.  If the
    database already exists, a confirmation whether to delete the database and
    recreate must be answered.
    '''
    if os.path.exists(filename):
        console = Console()
        answer = console.input(
            f"[bold red]Are you VERY sure you wish to delete {filename} and recreate?  Type YES to continue, any other input to exit:[/] "
        )
        if answer == "YES":
            rprint("[bold red]Deleting specified database.[/]")
            os.remove(filename)
        else:
            rprint("[bold blue]Exiting.[/]")
            raise typer.Exit()

    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.initialize_race_table(my_engine)
    rprint("[bold green]Completed setup of database.[/]")


@cli.command()
def add_coach(coach_csv: str, filename: str = "bb.db"):
    '''
    Command adds a coach record to the database.  The record should be
    a comma separated list as a quoted string.  The order of records is:
    "<Discord name>, <Blood Bowl 2 in-game name>, <Blood Bowl 3 in-game name>"
    '''
    my_engine = engine.initialize_engine(filename)
    engine.initialize_tables(my_engine)
    engine.add_coach(my_engine, coach_csv)


if __name__ == "__main__":
    cli()
