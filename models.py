import enum
from typing import List
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Race(Base):
    __tablename__ = "races"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    bb2: Mapped[bool] = mapped_column(Boolean)
    bb3: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"Row ID: {self.id}, Race name: {self.name}, In BB2?: {self.bb2}, In BB3?: {self.bb3}"


class Coach(Base):
    __tablename__ = "coaches"
    id: Mapped[int] = mapped_column(primary_key=True)
    d_name: Mapped[str] = mapped_column(String, nullable=False)
    bb2_name: Mapped[Optional[str]] = mapped_column(String)
    bb3_name: Mapped[Optional[str]] = mapped_column(String)

    @classmethod
    def from_str(cls, coach_str):
        """
        Receives a string containing comma separated values of the in-game
        coach name and the Discord user name.  Splits the string and returns a
        Coach object.

        :classmethod:
        :param str coach_str: The coach information in a CSV string, containing an in-game name and Discord name.
        :return: Returns an object of the Coach class.
        :rtype: Coach()
        """
        coach_list = coach_str.split(",")
        return cls(d_name=coach_list[0].lstrip(), bb2_name=coach_list[1].lstrip(), bb3_name=coach_list[2].lstrip())


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"))


class GameState(enum.Enum):
    UNPLAYED = "Unplayed"
    PLAYED = "Played"
    CONCESSION = "Concession"


class TourneyState(enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Tournament(Base):
    __tablename__ = "tournaments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    num_teams: Mapped[int] = mapped_column(Integer)
    num_rounds: Mapped[int] = mapped_column(Integer)
    current_round: Mapped[int] = mapped_column(Integer)
    state: Mapped[TourneyState]


class TourneyTeam(Base):
    __tablename__ = "tourneyteams"
    id: Mapped[int] = mapped_column(primary_key=True)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    tour_id: Mapped[int] = mapped_column(ForeignKey("tournaments.id"))
    round_num: Mapped[int] = mapped_column(Integer)
    home_id: Mapped[int] = mapped_column(ForeignKey("tourneyteams.id"))
    visitor_id: Mapped[int] = mapped_column(ForeignKey("tourneyteams.id"))
    gamestate: Mapped[GameState]
    home_score: Mapped[int] = mapped_column(Integer)
    visitor_score: Mapped[int] = mapped_column(Integer)
