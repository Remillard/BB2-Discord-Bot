#! python3
"""This module implements classes and methods for manipulating Blood Bowl 2
team names and league schedules in order to facilitate command line operation
and a Discord Bot API in the future."""
import sys
import argparse
import yaml

################################################################################
class Team:
    """Class encapsulates team data as well as multiple methods for
    constructing the object from different sources."""

    def __init__(self, name, race, coach, dtag):
        self.name = name
        self.race = race
        self.coach = coach
        self.dtag = dtag

    @classmethod
    def from_dict(cls, team_info):
        """Returns a class object filled with data from a dictionary (the
        format the YAML file will return)."""
        return cls(
            team_info["name"], team_info["race"], team_info["coach"], team_info["dtag"]
        )

    @classmethod
    def from_str(cls, team_str):
        """Returns a class object filled with data from a string (the
        format when creating a team from the command line)."""
        team_list = team_str.split(",")
        if team_list[2].lstrip() == "AI":
            return cls(
                team_list[0].lstrip(),
                team_list[1].lstrip(),
                team_list[2].lstrip(),
                "None",
            )
        return cls(
            team_list[0].lstrip(),
            team_list[1].lstrip(),
            team_list[2].lstrip(),
            team_list[3].lstrip(),
        )

    @property
    def yaml(self):
        """Returns a dictionary object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return {
            "name": self.name,
            "race": self.race,
            "coach": self.coach,
            "dtag": self.dtag,
        }


class League(list):
    """A customized list class encapsulating specific method for constructing
    the class out of a dictionary and Team objects.  May have additional
    custom methods later."""

    def __init__(self, teams_dict):
        super().__init__()
        for team_dict in teams_dict:
            self.append(Team.from_dict(team_dict))

    @property
    def yaml(self):
        """Returns a list object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return [team.yaml for team in self]


################################################################################
class Game:
    """Class that encapsulates the data pertaining to a single game in a
    tournament structure."""

    def __init__(self, game_data, league):
        """Initialization of Game object.  Keeping the Team object associated
        with each position as well as the index.  The index is used for
        recreating the YAML object."""
        self.home_index = game_data["home"]
        self.away_index = game_data["away"]
        self.home = league[game_data["home"]]
        self.away = league[game_data["away"]]

    @property
    def yaml(self):
        """Returns a dictionary object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return {"home": self.home_index, "away": self.away_index}


class Week(list):
    """Class that encapsulates the data pertaining to a single week in a
    tournament structure."""

    def __init__(self, game_list, league):
        super().__init__()
        for game in game_list:
            self.append(Game(game, league))

    @property
    def yaml(self):
        """Returns a list object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return [game.yaml for game in self]


class Schedule(list):
    """Class that encapsulates the data holding every week (and then every
    subsequent game) in a tournament structure."""

    def __init__(self, schedule_dict, league):
        super().__init__()
        for week in schedule_dict:
            self.append(Week(schedule_dict[week], league))

    @property
    def yaml(self):
        """Returns a dictionary object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return {f"week_{idx}": week.yaml for (idx, week) in enumerate(self)}


################################################################################
class TourneyFile:
    """Class encapculations interactions with the YAML file.  No one outside
    of this class ought to be exposed to THE BLOB."""

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "r") as f:
            blob = yaml.safe_load(f)
        self.league = League(blob["teams"])
        self.schedule = Schedule(blob["schedule"], self.league)
        self.current_week = blob["current_week"]
        return self.league, self.schedule, self.current_week

    def write(self, blob):
        with open(self.filename, "w") as f:
            yaml.dump(blob, f)

    def create(self):
        blob = {"current_week": 0, "teams": None, "schedule": None}
        self.write(blob)

    def add_team(self, team_str):
        self.read()
        self.league.append(Team.from_str(team_str))
        self.write(self.make_blob)

    def del_team(self, team_name):
        self.read()
        for idx, team in enumerate(self.league):
            if team.name == team_name:
                del self.league[idx]
                self.write(self.make_blob)
                break
        else:
            print(f"Team {team_name} not found!")

    def incr_week(self):
        self.read()
        self.current_week += 1
        self.write(self.make_blob)

    @property
    def make_blob(self):
        return {
            "current_week": self.current_week,
            "teams": self.league.yaml,
            "schedule": self.schedule.yaml,
        }


################################################################################
def report_teams(tfile):
    league, schedule, current_week = tfile.read()
    print(f"Number of teams: {len(league)}")
    for idx, team in enumerate(league):
        print(f"-- Team #{idx} ---------------------------")
        print(f"Team Name: {team.name}")
        print(f"Team Race: {team.race}")
        print(f"Coach Name: {team.coach}")
        print(f"Coach Discord Tag: {team.dtag}")


def report_schedule(tfile):
    league, schedule, current_week = tfile.read()
    print(f"Number of weeks in the schedule: {len(schedule)}")
    for idx, week in enumerate(schedule):
        print(f"-- Week #{idx} ---------------------------")
        for game in week:
            print(f"Home: {game.home.name:40} Away: {game.away.name:40}")


################################################################################
def main():
    parser = argparse.ArgumentParser(
        prog="bb2_bot",
        description="Program to manipulate a Blood Bowl 2 tournament data file.",
    )
    parser.add_argument("filename", help="The tournament data file (YAML format).")
    parser.add_argument(
        "--create",
        action="store_true",
        help="Creates a base tournament file (YAML format).",
    )
    parser.add_argument(
        "--add_team",
        help='''Adds a team to the tournament.  Format should be a comma
        separated list inside quotes in the following order:  "Team Name, Race,
        Coach Name, Coach Discord Tag".  If the coach is an AI team, use "AI"
        for the Coach Name field, and leave off the Discord Tag field.
        Example #1 --add_team "Super Joes, Khemri, John Doe, JDoe#9999"
        Example #2 --add_team "Doofus Name, Human, AI"''',
    )
    parser.add_argument(
        "--del_team",
        help="""Removes a team from the list.  Team should be specified by
        team name.  If there are spaces in the name, please surround the name
        with quotes.""",
    )
    parser.add_argument(
        "--report",
        choices=["teams", "schedule", "full"],
        help="Produces the selected report for the tournament.",
    )
    args = parser.parse_args()

    tfile = TourneyFile(args.filename)

    if args.create:
        tfile.create()
    elif args.add_team:
        tfile.add_team(args.add_team)
    elif args.del_team:
        tfile.del_team(args.del_team)
    elif args.report == "teams":
        print("======================================")
        report_teams(tfile)
    elif args.report == "schedule":
        print("======================================")
        report_schedule(tfile)
    elif args.report == "full":
        print("======================================")
        report_teams(tfile)
        print("======================================")
        report_schedule(tfile)


################################################################################
if __name__ == "__main__":
    main()
