#! python3
import sys
import os.path
from os import path
import argparse
import yaml

class Team:
    def __init__(self, name, race, coach, dtag):
        self.name = name
        self.race = race
        self.coach = coach
        self.dtag = dtag

    @classmethod
    def from_dict(cls, team_info):
        #print(team_info)
        return cls(team_info["name"], team_info["race"], team_info["coach"], team_info["dtag"])

    @classmethod
    def from_str(cls, team_str):
        team_list = team_str.split(',')
        return cls(team_list[0].lstrip(), team_list[1].lstrip(), team_list[2].lstrip(), team_list[3].lstrip())

    @property
    def to_dict(self):
        return {'name' : self.name, 'race' : self.race, 'coach': self.coach, 'dtag' : self.dtag}


def report_teams(filename):
    teams = []
    with open(filename, "r") as f:
        blob = yaml.safe_load(f)
    print(f"Number of teams: {blob['num_teams']}")
    for team_dict in blob["teams"]:
        team = Team.from_dict(team_dict)
        teams.append(team)
    for team in teams:
        print("-----------------------------")
        print(f"Team Name: {team.name}")
        print(f"Team Race: {team.race}")
        print(f"Coach Name: {team.coach}")
        print(f"Coach Discord Tag: {team.dtag}")
    # print("------------------------------------")
    # for week in blob["schedule"]:
    #     for game in blob["schedule"][week]:
    #         print(
    #             f"Game: {game} -- Home Team: {blob['schedule'][week][game]['home']} -- Away Team: {blob['schedule'][week][game]['away']}"
    #         )


def create_tfile(filename):
    """pass"""
    blob = {"num_teams": 0, "teams": None, "schedule": None}
    with open(filename, "w") as f:
        yaml.dump(blob, f)

def add_team(filename, team_str):
    team = Team.from_str(team_str)
    with open(filename, 'r') as f:
        blob = yaml.safe_load(f)
    blob['num_teams'] += 1
    if blob['teams'] is not None:
        blob['teams'].append(team.to_dict)
    else:
        blob['teams'] = [team.to_dict]
    with open(filename, 'w') as f:
        yaml.dump(blob, f)


def main():
    parser = argparse.ArgumentParser(
        prog="bb2_tourney",
        description="Program to manipulate a Blood Bowl 2 tournament data file.",
    )
    parser.add_argument("filename", help="The tournament data file in YAML format.")
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="Creates a base tournament YAML file.",
    )
    parser.add_argument(
        "-at",
        "--add_team",
        help='Adds a team to the tournament.  Format should be a comma separated list inside quotes.  Team Name, Race, Coach Name, Coach Discord Tag.  Example --add_team "Super Joes, Khemri, John Doe, JDoe#9999"'
    )
    parser.add_argument(
        "-rt",
        "--report_teams",
        action="store_true",
        help="Produces a report on teams in the tournament.",
    )
    args = parser.parse_args()

    if args.report_teams:
        report_teams(args.filename)
    elif args.create:
        create_tfile(args.filename)
    elif args.add_team:
        add_team(args.filename, args.add_team)


if __name__ == "__main__":
    main()
