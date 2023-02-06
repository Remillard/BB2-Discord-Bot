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
    # Convert from the CSV variation
    coach_list = [str(i.lstrip()) or None for i in coach_csv.split(",")]
    # Determine first if the coach may already exist in the database.
    try:
        find_coach(engine, coach_list[0], fuzzy=0)
    except KeyError:
        # If it's not found then it's okay to add the coach to the database.
        coach = models.Coach()
        coach.d_name = coach_list[0]
        coach.bb2_name = coach_list[1]
        coach.bb3_name = coach_list[2]
        with Session(engine) as session:
            session.add(coach)
            session.commit()
    else:
        print(
            f"[bold red]Coach {this_coach.d_name} already exists.  Nothing added to database![/]"
        )


def find_coach(engine, d_name, fuzzy=1):
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
    :param int fuzzy: An integer controlling fuzzy finding and when exceptions
                      are raised.  Default = 1, closest match with no interaction.
                      0 = Exact Match Only.
                      1 = Only one match permitted (no interaction with user)
                      2 = Multiple matches permitted, asks user for input.
    :return: A tuple containing a Coach object as its only member.
    """
    with Session(engine) as session:
        # Exact match statement
        # The Result.all() is a list of tuples.  Each tuple contains one table
        # object.  This is important for the referencing below because it's
        # fucking maddening.  We return the tuple.
        stmt = select(models.Coach).where(models.Coach.d_name == d_name)
        coaches = session.execute(stmt).all()
        # Under every circumstance, if the exact match works, we use that one
        # with no further thought.
        if coaches is not None and len(coaches) == 1:
            print("[green]Found exact coach match![/]")
            return coaches[0]
        elif fuzzy == 0:
            # Exact match failed at this point.  If we've only permitted exact
            # (fuzzy = 0) then we raise exception here.  Otherwise we continue with
            # a fuzzy search.
            raise KeyError(f'Could not find the coach name string: "{d_name}".')
        elif fuzzy in [1, 2]:
            # Wildcard variation.
            print("[bold red]Exact match failed.  Trying fuzzy match.[/]")
            stmt = select(models.Coach).where(models.Coach.d_name.like(f"%{d_name}%"))
            coaches = session.execute(stmt).all()
            # Under fuzzy circumstances, if we've found exactly one fuzzy match,
            # we use that one with no further thought.
            if coaches is not None and len(coaches) == 1:
                print(
                    f"[green]{len(coaches)} record matches.  Using {coaches[0][0].d_name}.[/]"
                )
                return coaches[0]
            elif fuzzy == 1:
                # Exactly one fuzzy match failed, so we raise exception.
                raise KeyError(f'Could not find the coach name string: "{d_name}".')
            elif fuzzy == 2 and coaches is not None:
                # Multiple matches permitted, user queried for exact.
                print(f"[bold red]{len(coaches)} records match.[/]")
                for row in coaches:
                    if Confirm.ask(f"[cyan]Select {row[0].d_name}?", default=False):
                        print(f"[green]Using {row[0].d_name}.")
                        return row
                else:
                    raise KeyError(f'Could not find the coach name string "{d_name}".')
        else:
            raise KeyError(f'Could not find the coach name string: "{d_name}".')


def find_race(engine, r_name, fuzzy=1):
    """
    Receives the engine and a possible racial name along with a boolean that
    sets whether or not the fuzzy finding method is used.  The method will first
    search for an exact match.  If that fails, the method will assume the text
    is a fragment and try to find records(s) matching.  If no match is found, an
    exception is raised.  If a single match is found, that one will be returned.
    If more than one match is found, the CLI will be queried for each match.  If
    none of the matches are chosen as correct, an exception is raised.

    :param engine: An object from SQLAlchemy create_engine method.
    :param str race: The name of the team race.
    :param int fuzzy: An integer controlling fuzzy finding and when exceptions
                      are raised.  Default = 1, closest match with no interaction.
                      0 = Exact Match Only.
                      1 = Only one match permitted (no interaction with user)
                      2 = Multiple matches permitted, asks user for input.
    :return: A SQLAlchemy Result object.

    """
    with Session(engine) as session:
        # Exact match statement The Result.all() is a list of tuples.  Each
        # tuple contains one table object.  We return the tuple.
        stmt = select(models.Race).where(models.Race.name == r_name)
        races = session.execute(stmt).all()
        # Under every circumstance, if the exact match works, we use that one
        # with no further thought.
        if races is not None and len(races) == 1:
            print("[green]Found exact race match![/]")
            return races[0]
        elif fuzzy == 0:
            # Exact match failed at this point.  If we've only permitted exact
            # (fuzzy = 0) then we raise exception here.  Otherwise we continue with
            # a fuzzy search.
            raise KeyError(f'Could not find the race name string: "{r_name}".')
        elif fuzzy in [1, 2]:
            # Wildcard variation.
            print("[bold red]Exact match failed.  Trying fuzzy match.[/]")
            stmt = select(models.Race).where(models.Race.name.like(f"%{r_name}%"))
            races = session.execute(stmt).all()
            # Under fuzzy circumstances, if we've found exactly one fuzzy match,
            # we use that one with no further thought.
            if races is not None and len(races) == 1:
                print(
                    f"[green]{len(races)} record matches.  Using {races[0][0].name}.[/]"
                )
                return races[0]
            elif fuzzy == 1:
                # Exactly one fuzzy match failed, so we raise exception.
                raise KeyError(f'Could not find the race name string: "{r_name}".')
            elif fuzzy == 2 and races is not None:
                # Multiple matches found and permitted.  User queried.
                print(f"[bold red]{len(races)} record matches.[/]")
                for row in races:
                    if Confirm.ask(f"[cyan]Select {row[0].name}?", default=False):
                        print(f"[green]Using {row[0].name}.")
                        return row
                else:
                    raise KeyError(f'Could not find the race name string "{r_name}".')
            else:
                raise KeyError(f'Could not find the race name string: "{r_name}".')


def add_team(engine, team_csv, fuzzy=1):
    """
    Receives the engine and a CSV string of coach Discord Name, Team Name,
    Race, and Game Version and creates a record in the Team table.
    "<coach_name>, <team_name>, <race_name>, <version (2 or 3)>"

    :param engine: An object from SQLAlchemy create_engine method.
    :param str team_str: A string with comma separated values for the fields.
    """
    team_list = [str(i.lstrip()) or None for i in team_csv.split(",")]
    coach = find_coach(engine, team_list[0], fuzzy)
    race = find_race(engine, team_list[2], fuzzy)
    # Each of the finds will raise exception if nothing found, so we don't
    # really have to check for None at this point.
    team = models.Team(
        name=team_list[1],
        bb_ver=team_list[3],
        coach_id=coach[0].id,
        race_id=race[0].id,
    )
    with Session(engine) as session:
        session.add(team)
        session.commit()


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


def get_all_teams(engine):
    team_list = []
    with Session(engine) as session:
        stmt = (
            select(models.Team, models.Coach, models.Race)
            .join(models.Coach)
            .join(models.Race)
        )
        result = session.execute(stmt)
        for obj in result:
            team_list.append(
                [
                    obj.Team.id,
                    obj.Team.name,
                    obj.Race.name,
                    obj.Team.bb_ver,
                    obj.Coach.d_name,
                ]
            )
    return team_list


def add_tournament(engine, tour_csv):
    tour_list = [str(i.lstrip()) or None for i in tour_csv.split(",")]
    tour = models.Tournament(
        name=tour_list[0],
        bb_ver=tour_list[1],
        mode=models.TourneyMode(tour_list[2]),
        num_teams=tour_list[3],
        num_rounds=tour_list[4],
    )
    with Session(engine) as session:
        session.add(tour)
        session.commit()


def get_all_tournaments(engine):
    tour_list = []
    with Session(engine) as session:
        stmt = select(models.Tournament)
        result = session.execute(stmt)
        for tour_obj in result.scalars():
            tour_list.append(tour_obj)
    return tour_list
