#! python3
################################################################################
# SQLModel Model/Table Definitions
################################################################################
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

################################################################################
# Enumerated Types Static Tables
################################################################################
class Race(SQLModel, table=True):
    __tablename__ = "races"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    bb2: int
    bb3: int

    def my_model_method(self):
        print(f"Hi, I'm {self.name}.")

    def __str__(self):
        return f"Race: {self.name}.  Blood Bowl 2: {self.bb2}.  Blood Bowl 3:{self.bb3}"


################################################################################
class TourneyState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    state: str


################################################################################
class GameState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    state: str


################################################################################
# Operational Tables
################################################################################
class Coach(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    d_name: str
    bb2_name: Optional[str] = None
    bb3_name: Optional[str] = None


################################################################################
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    bb_ver: int
    race_id: int = Field(foreign_key="races.id")
    coach_id: int = Field(foreign_key="coach.id")


################################################################################
class Tournament(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    bb_ver: int
    ttype: int
    tstate: int = Field(default=1)
    num_teams: int
    num_rounds: int
    current_round: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


################################################################################
class TournamentTeam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tour_id: int = Field(foreign_key="tournament.id")
    team_id: int = Field(foreign_key="team.id")


################################################################################
class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tour_id: int = Field(foreign_key="tournament.id")
    round_num: int
    home_id: int = Field(foreign_key="tournamentteam.id")
    visitor_id: int = Field(foreign_key="tournamentteam.id")
    gamestate_id: int = Field(default=1, foreign_key="gamestate.id")
    home_score: Optional[int] = None
    visitor_score: Optional[int] = None
