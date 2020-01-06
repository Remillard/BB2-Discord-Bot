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

    def __init__(self, teams_dict=None):
        # Expect to receive nothing and initialize an empty list, or a list
        # of dictionary objects that must be parsed and then we fill our
        # list with Team objects.
        super().__init__()
        teams_dict = teams_dict or []
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

    def __init__(self, game_data):
        """Initialization of Game object.  Keeping the Team object associated
        with each position as well as the index.  The index is used for
        recreating the YAML object."""
        self.home_index = game_data["home"]
        self.away_index = game_data["away"]
        self.home = None
        self.away = None

    def add_team_data(self, league):
        """Method contains a Team object for the purposes of reporting and
        matching an index number to a Team name."""
        self.home = league[self.home_index]
        self.away = league[self.away_index]

    @property
    def yaml(self):
        """Returns a dictionary object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return {"home": self.home_index, "away": self.away_index}


class Week(list):
    """Class that encapsulates the data pertaining to a single week in a
    tournament structure."""

    def __init__(self, game_list):
        super().__init__()
        for game in game_list:
            self.append(Game(game))

    @property
    def yaml(self):
        """Returns a list object to be used to create the data structure
        that is built up into the final overall YAML structure."""
        return [game.yaml for game in self]


class Schedule(list):
    """Class that encapsulates the data holding every week (and then every
    subsequent game) in a tournament structure."""

    def __init__(self, schedule_dict=None):
        # Again we expect to get either nothing, or a dictionary with
        # keys labeling the weeks.
        super().__init__()
        schedule_dict = schedule_dict or {}
        for week in schedule_dict:
            self.append(Week(schedule_dict[week]))

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
        self.league = League()
        self.schedule = Schedule()
        self.current_week = 0

    def read(self):
        """Reading the YAML file and parsing the results.  Have to check
        to make sure fields are populated before creating the data structures.
        """
        with open(self.filename, "r") as f:
            blob = yaml.safe_load(f)
        # Checking the population of the blob against these keys.  The
        # list initializer does not like None as an input.
        if blob["teams"]:
            self.league = League(blob["teams"])
        if blob["schedule"]:
            self.schedule = Schedule(blob["schedule"])
        if blob["current_week"]:
            self.current_week = blob["current_week"]
        return self.league, self.schedule, self.current_week

    def write(self, blob):
        """Encapsulated YAML writing method."""
        with open(self.filename, "w") as f:
            yaml.dump(blob, f)

    def create(self):
        """Encapsulated YAML initial file state method."""
        # blob = {"current_week": 0, "teams": None, "schedule": None}
        self.write(self.make_blob)

    def add_team(self, team_str):
        """Encapsulated team addition method."""
        self.read()
        self.league.append(Team.from_str(team_str))
        self.write(self.make_blob)

    def del_team(self, team_name):
        """Encapsulated team deletion method."""
        self.read()
        print(f"self.league is {self.league}")
        for idx, team in enumerate(self.league):
            if team.name == team_name:
                del self.league[idx]
                self.write(self.make_blob)
                break
        else:
            print(f"Team {team_name} not found!")

    def incr_week(self):
        """Method to increment the current week."""
        self.read()
        self.current_week += 1
        self.write(self.make_blob)

    @property
    def make_blob(self):
        """Method that constructs the YAML data block (the "blob") from our
        internal data state."""
        teams_result = None
        if self.league is not None:
            teams_result = self.league.yaml
        schedule_result = None
        if self.schedule is not None:
            schedule_result = self.schedule.yaml
        return {
            "current_week": self.current_week,
            "teams": teams_result,
            "schedule": schedule_result,
        }


################################################################################
def report_teams(tfile):
    """Method to print a report for the team data structures retrieved from the
    YAML file."""
    league, schedule, current_week = tfile.read()
    print(f"Number of teams: {len(league)}")
    for idx, team in enumerate(league):
        print(f"-- Team #{idx} ---------------------------")
        print(f"Team Name: {team.name}")
        print(f"Team Race: {team.race}")
        print(f"Coach Name: {team.coach}")
        print(f"Coach Discord Tag: {team.dtag}")


def report_schedule(tfile):
    """Method to print a report of the schedule data retrieved from the YAML
    file."""
    league, schedule, current_week = tfile.read()
    print(f"Number of weeks in the schedule: {len(schedule)}")
    for idx, week in enumerate(schedule):
        print(f"-- Week #{idx} ---------------------------")
        for game in week:
            game.add_team_data(league)
            print(f"Home: {game.home.name:40} Away: {game.away.name:40}")


################################################################################
def main():
    """Main command line entry point."""
    parser = argparse.ArgumentParser(
        prog="bb_tournament",
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
    parser.add_argument(
        "--add_week",
        action="store_true",
        help="""Adds a week to the current schedule.""",
    )
    parser.add_argument(
        "--add_game",
        help="""Adds any number of games to the week.  Should be followed by a
        list of numbers corresponding to team indexes (as seen by --report
        teams).  The numbers are interpreted as pairs, home team first,
        followed by the away team.  If an odd number of teams are added, the
        last team in the list is given a 'bye' game for the week.  Example #1
        --add_game 0 1 2 3 4 5 will produce 3 games in the week with Team 0
        playing at home against Team 1 playing away, and so on with pairings,
        2 vs 3, and 4 vs 5.  Example #2 --add_game 3 2 1 4 5 will produce three
        games, 3 vs 2, 1 vs 4, and Team 5 gets a bye.""",
    )
    args = parser.parse_args()

    tfile = TourneyFile(args.filename)

    if args.create:
        tfile.create()
    if args.add_team:
        tfile.add_team(args.add_team)
    if args.del_team:
        tfile.del_team(args.del_team)
    if args.report == "teams":
        print("======================================")
        report_teams(tfile)
    if args.report == "schedule":
        print("======================================")
        report_schedule(tfile)
    if args.report == "full":
        print("======================================")
        report_teams(tfile)
        print("======================================")
        report_schedule(tfile)


################################################################################
if __name__ == "__main__":
    main()
