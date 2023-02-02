from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from rich import print
from rich.prompt import Confirm

import models
import sql_strings as sqlstr


def initialize_engine(filename):
    """
    Creates the local engine instance from the given filename.

    :param string filename: Filename of the SQLite3 database to use.
    """
    return create_engine(f"sqlite+pysqlite:///{filename}", echo=False)


def initialize_tables(engine):
    """
    Method initializes the models and creates tables only if needed.

    :param engine: An object from SQLAlchemy create_engine method.
    """
    models.Base.metadata.create_all(engine)


def initialize_race_table(engine):
    """
    Method fills the race table with data.  Should only be run once at
    database creation.
    :param engine: An object from SQLAlchemy create_engine method.
    """
    with Session(engine) as session:
        for row in sqlstr.initial_race_table:
            race = models.Race(name=row[0], bb2=row[1], bb3=row[2])
            session.add(race)
        session.commit()


def add_coach(engine, coach_csv):
    """
    Receives the engine and a string of comma separated values for the coach
    Discord name, Blood Bowl 2 in-game coach name (if any) and Blood Bowl 3
    in-game name (if any).

    :param engine: An object from SQLAlchemy create_engine method.
    :param str coach_csv: A string with comma separated values for the three
                          fields.
    """
    # Determine first if the coach may already exist in the database.
    this_coach = models.Coach.from_str(coach_csv)
    if find_coach(engine, this_coach.d_name, fuzzy=False) is None:
        with Session(engine) as session:
            session.add(this_coach)
            session.commit()
    else:
        print(f"[bold red]Coach {this_coach.d_name} already exists.  Nothing added to database![/]")


def find_coach(engine, d_name, fuzzy=True):
    """
    Receives the engine and a possible Discord name.  The method will first
    assume that the name is exact and will search for it and return the first
    record (this column must be unique).  If that fails, the method will assume
    the text is a fragment and try to find record(s) matching.  If no match is
    found, an exception is raised.  If a single match is found, that one will be
    returned.  If more than one match is found, the CLI will be queried for each
    match.  If none of the matches are chosen as correct, an exception is
    raised.

    :param engine: An object from SQLAlchemy create_engine method.
    :param str d_name: The Discord name of a coach.
    :param bool fuzzy: A boolean that represents whether fuzzy finding is accepted.
    :return: A tuple containing a Coach object as its only member.
    """
    with Session(engine) as session:
        stmt = select(models.Coach).where(models.Coach.d_name == d_name)
        coach = session.execute(stmt).first()
        if not fuzzy:
            return coach
        else:
            if coach is not None:
                print("[green]Found exact coach match![/]")
                return coach
            else:
                print("[bold red]Exact match failed.  Trying fuzzy match.[/]")
                stmt = select(models.Coach).where(models.Coach.d_name.like(f"%{d_name}%"))
                # The coaches result is a list of tuples.  Each tuple contains one table
                # object.  This is important for the referencing below because it's
                # fucking maddening.  We return the tuple.
                coaches = session.execute(stmt).all()
                if coaches is None:
                    raise KeyError(f'Could not find the coach name string: "{d_name}".')
                elif len(coaches) == 1:
                    print(f"[green]{len(coaches)} record matches.  Using {coaches[0][0].d_name}.[/]")
                    return coaches[0]
                else:
                    print(f"[bold red]{len(coaches)} records match.[/]")
                    for row in coaches:
                        if Confirm.ask(f"[cyan]Select {row[0].d_name}?", default=False):
                            print(f"[green]Using {row[0].d_name}.")
                            return row
                    else:
                        raise KeyError(f'Could not find the coach name string "{d_name}".')


def find_race(engine, race):
    """
    Receives the engine and a racial name and produces the first record
    that matches, or returns None.

    :param engine: An object from SQLAlchemy create_engine method.
    :param str race: The name of the team race.
    :return: A SQLAlchemy Result object.
    """
    with Session(engine) as session:
        stmt = select(models.Race).where(models.Race.name == race)
        race = session.execute(stmt).first()
        return race


def add_team(engine, team_csv):
    """
    Receives the engine and a CSV string of coach Discord Name, Team Name,
    and Race, and creates a record in the Team table.

    :param engine: An object from SQLAlchemy create_engine method.
    :param str team_str: A string with comma separated values for the fields.
    """
    team_list = [str(i.lstrip()) or None for i in team_csv.split(",")]
    coach = find_coach(engine, team_list[0])
    race = find_race(engine, team_list[2])
    if coach is not None and race is not None:
        team = models.Team(name=team_list[1], coach_id=coach[0].id, race_id=race[0].id)
        with Session(engine) as session:
            session.add(team)
            session.commit()
    else:
        print("Team information invalid.")


def get_all_coaches(engine):
    coach_list = []
    with Session(engine) as session:
        stmt = select(models.Coach)
        result = session.execute(stmt)
        # The result object must be used before the session ends as it becomes
        # invalid at that point.
        for coach_obj in result.scalars():
            coach_list.append(coach_obj)
    return coach_list


# NOTES: This SQL command lists teams and coaches:
# select teams.id, teams.name, coaches.d_name from teams inner join coaches on coaches.id=teams.coach_id;
