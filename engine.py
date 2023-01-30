from sqlalchemy import create_engine

filename = "bb.db"

import models

def initialize_tables(engine):
    models.Base.metadata.create_all(engine)

def initialize_engine(filename):
    return create_engine(f"sqlite+pysqlite:///{filename}", echo=True)


    
