#! python3
"""
Data Structures for dealing with Blood Bowl 2 Teams
"""
import argparse
from ruamel.yaml import YAML

class Team():
    """Class that holds the information about a team in Blood Bowl 2"""
    def __init__(self, name, dtag, coach_name, team_name, team_race):
        """Initializes the class"""
        self.name = name
        self.dtag = dtag
        self.coach_name = coach_name
        self.team_name = team_name
        self.team_race = team_race

    def __str__(self):
        """Class printing method"""
        return f'{self.name} {self.dtag} {self.coach_name} {self.team_name} {self.team_race}'


def main():
    """Main command line entry point"""
    parser.argparse.ArgumentParser(prog="bb2_teams", description="More here later")
    parser.add_argument()

    yaml = YAML()
    tfile = open("sample_tourney.yaml")
    blob = yaml.load(tfile)
    tfile.close()
    # print(blob)
    # print(blob['num_teams'])
    # print(blob['teams'])
    print(f"Number of teams: {blob['num_teams']}")
    for team in blob['teams']:
        print("---")
        print(f"Team Index: {team}")
        print("---")
        team_info = blob['teams'][team]
        print(f"Team Name: {team_info['name']}")
        print(f"Team Race: {team_info['race']}")
        print(f"Coach Name: {team_info['coach_name']}")
        print(f"Coach Discord Tag: {team_info['dtag']}")
    print("------------------------------------")
    for week in blob['schedule']:
        for game in blob['schedule'][week]:
            print(f"Game: {game} -- Home Team: {blob['schedule'][week][game]['home']} -- Away Team: {blob['schedule'][week][game]['away']}")


if __name__ == '__main__':
    main()
