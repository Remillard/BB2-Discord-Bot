#! python3
import os.path
from os import path
import argparse
from ruamel.yaml import YAML


class Team:
    def __init__(self, team_info):
        self.name = team_info["name"]
        self.race = team_info["race"]
        self.coach_name = team_info["coach_name"]
        self.dtag = team_info["dtag"]


def report_teams(filename):
    teams = []
    yaml = YAML()
    yaml.version = (1, 2)
    with open(filename, "r") as f:
        blob = yaml.load(f)
    print(f"Number of teams: {blob['num_teams']}")
    for team_block in blob["teams"]:
        team = Team(blob["teams"][team_block])
        teams.append(team)
    for team in teams:
        print("-----------------------------")
        print(f"Team Name: {team.name}")
        print(f"Team Race: {team.race}")
        print(f"Coach Name: {team.coach_name}")
        print(f"Coach Discord Tag: {team.dtag}")
    # print("------------------------------------")
    # for week in blob["schedule"]:
    #     for game in blob["schedule"][week]:
    #         print(
    #             f"Game: {game} -- Home Team: {blob['schedule'][week][game]['home']} -- Away Team: {blob['schedule'][week][game]['away']}"
    #         )


def main():
    parser = argparse.ArgumentParser(
        prog="bb2_tourney",
        description="Program to manipulate a Blood Bowl 2 tournament data file.",
    )
    parser.add_argument("filename", help="The tournament data file in YAML format.")
    parser.add_argument(
        "-rt",
        "--report_teams",
        action="store_true",
        help="Produces a report on teams in the tournament.",
    )
    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="Creates a base tournament YAML file."
    )
    args = parser.parse_args()

    if args.report_teams:
        report_teams(args.filename)


if __name__ == "__main__":
    main()
