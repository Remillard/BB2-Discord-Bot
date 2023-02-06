import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session


class Base(DeclarativeBase):
    pass


class MyTable(Base):
    __tablename__ = "my_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


def initialize_engine(filename):
    return create_engine(f"sqlite+pysqlite:///{filename}", echo=True)


def initialize_tables(engine):
    Base.metadata.create_all(engine)


def add_row(engine, name):
    this_row = MyTable(name=name)
    print(this_row)
    with Session(engine) as session:
        session.add(this_row)
        session.commit()


my_file = "test.db"

my_engine = initialize_engine(my_file)
initialize_tables(my_engine)

add_row(my_engine, "Dave")
