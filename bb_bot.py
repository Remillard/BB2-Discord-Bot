#! python3
import sys
import os.path
from os import path
import argparse
import yaml


class TourneyYAML:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, "r") as f:
            blob = yaml.safe_load(f)
        return blob

    def write(self, blob):
        with open(self.filename, "w") as f:
            yaml.dump(blob, f)


class Team:
    def __init__(self, name, race, coach, dtag):
        self.name = name
        self.race = race
        self.coach = coach
        self.dtag = dtag

    @classmethod
    def from_dict(cls, team_info):
        # print(team_info)
        return cls(
            team_info["name"], team_info["race"], team_info["coach"], team_info["dtag"]
        )

    @classmethod
    def from_str(cls, team_str):
        team_list = team_str.split(",")
        if team_list[2].lstrip() != "AI":
            return cls(
                team_list[0].lstrip(),
                team_list[1].lstrip(),
                team_list[2].lstrip(),
                team_list[3].lstrip(),
            )
        else:
            return cls(
                team_list[0].lstrip(),
                team_list[1].lstrip(),
                team_list[2].lstrip(),
                "None",
            )

    @property
    def to_dict(self):
        return {
            "name": self.name,
            "race": self.race,
            "coach": self.coach,
            "dtag": self.dtag,
        }


class League:
    def __init__(self, teams_dict):
        for team_dict in teams_dict:
            self.teams = []
            self.teams.append(Team.from_dict(team_dict))

    def __iter__(self):
        return LeagueIterator(self)

class LeagueIterator():
    def __init__(self, league):
        self.league = league
        self.index = 0

    def __next__(self):
        if self.index < len(self.league.teams):
            result = self.league.teams[self.index]
            self.index += 1
            return result
        raise StopIteration


def report_teams(tfile):
    blob = tfile.read()
    print(f"Number of teams: {blob['num_teams']}")
    league = League(blob["teams"])
    for idx, team in enumerate(league):
        print(f"-- Team #{idx} ---------------------------")
        print(f"Team Name: {team.name}")
        print(f"Team Race: {team.race}")
        print(f"Coach Name: {team.coach}")
        print(f"Coach Discord Tag: {team.dtag}")


def report_schedule(tfile):
    blob = tfile.read()
    teams = Teams(blob["teams"])
    print(f"Number of weeks in the schedule: {blob['num_weeks']}")
    for idx, week in enumerate(blob["schedule"]):
        print(f"-- Week #{idx} ---------------------------")
        for game in blob["schedule"][week]:
            print(f"Home: {teams[game[0]].name:40} Away: {teams[game[1]].name:40}")


def create_tfile(tfile):
    blob = {"num_teams": 0, "num_weeks": 0, "teams": None, "schedule": None}
    tfile.write(blob)


def add_team(tfile, team_str):
    team = Team.from_str(team_str)
    blob = tfile.read()
    blob["num_teams"] += 1
    if blob["teams"] is not None:
        blob["teams"].append(team.to_dict)
    else:
        blob["teams"] = [team.to_dict]
    tfile.write(blob)


def del_team(tfile, team_name):
    blob = tfile.read()
    for idx, val in enumerate(blob["teams"]):
        if val["name"] == team_name:
            del blob["teams"][idx]
            blob["num_teams"] -= 1
            tfile.write(blob)
            break
    else:
        print(f"Team {team_name} not found!")


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
        help="Removes a team from the list.  Team should be specified by team name.  If there are spaces in the name, please surround the name with quotes.",
    )
    parser.add_argument(
        "--report",
        choices=["teams", "schedule", "full"],
        help="Produces the selected report for the tournament.",
    )
    args = parser.parse_args()

    tfile = TourneyYAML(args.filename)

    if args.create:
        create_tfile(tfile)
    elif args.add_team:
        add_team(tfile, args.add_team)
    elif args.del_team:
        del_team(tfile, args.del_team)
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


if __name__ == "__main__":
    main()
