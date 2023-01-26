#! python3
################################################################################
# Remodel Database Engine
################################################################################
import os
import argparse

from sqlmodel import SQLModel, Session, create_engine

import models

import sql_strings as sqlstr

################################################################################
def initialize_enum_tables(engine):
    with Session(engine) as session:
        for item in sqlstr.initial_gamestate_table:
            # The initial table was originally designed for a SQLite SQL VALUE
            # insertion through the sqlite3 library, so it's a list of tuples.
            abcd = models.GameState(state=item[0])
            session.add(abcd)
        for item in sqlstr.initial_tourneystate_table:
            tourstate = models.TourneyState(state=item[0])
            session.add(tourstate)
        for item in sqlstr.initial_race_table:
            race = models.Race(name=item[0], bb2=item[1], bb3=item[2])
            session.add(race)
        session.commit()


################################################################################
def initialize_db_and_tables(filename):
    sqlite_url = f"sqlite:///{filename}"
    engine = create_engine(sqlite_url, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine
