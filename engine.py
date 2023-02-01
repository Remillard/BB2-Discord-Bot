from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session

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
    if find_coach(engine, this_coach.d_name) is None:
        with Session(engine) as session:
            session.add(this_coach)
            session.commit()
    else:
        print("Coach already exists!  Nothing added to database.")


def find_coach(engine, d_name):
    """
    Receives the engine and a Discord name (these are required and must
    be unique) and produces the first record that matches, or returns None.

    :param engine: An object from SQLAlchemy create_engine method.
    :param str d_name: The Discord name of a coach.
    :return: A SQLAlchemy Result object.
    """
    with Session(engine) as session:
        stmt = select(models.Coach).where(models.Coach.d_name == d_name)
        coach = session.execute(stmt).first()
        return coach


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
    with Session(engine) as session:
        stmt = select(models.Coach)
        result = session.execute(stmt)
        for coach_obj in result.scalars():
            print(coach_obj)

# NOTES: This SQL command lists teams and coaches:
# select teams.id, teams.name, coaches.d_name from teams inner join coaches on coaches.id=teams.coach_id;
