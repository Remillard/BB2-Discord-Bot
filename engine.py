from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import models
import sql_strings as sqlstr


def initialize_engine(filename):
    """
    Creates the local engine instance from the given filename.

    :param string filename: Filename of the SQLite3 database to use.
    """
    return create_engine(f"sqlite+pysqlite:///{filename}", echo=True)


def initialize_tables(engine):
    """
    Method initializes the models and creates tables only if needed.

    :param engine: An object from SQLAlchemy create_engine method.
    """
    models.Base.metadata.create_all(engine)


def initialize_race_table(engine):
    """
    Method fills the race table with data.  Should only be run once at database creation.
    :param engine: An object from SQLAlchemy create_engine method.
    """
    with Session(engine) as session:
        for row in sqlstr.initial_race_table:
            race = models.Race(name=row[0], bb2=row[1], bb3=row[2])
            session.add(race)
        session.commit()
