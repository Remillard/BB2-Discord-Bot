#! python3
"""This module implements methods required to open a YAML file of Blood Bowl
trivia comments, and randomly select and print one."""
import argparse
import random
import yaml


################################################################################
class TriviaFile:
    """Class encapsulates interactions with the trivia YAML file."""

    def __init__(self, filename):
        self.filename = filename
        self.fileread = False
        self.trivia = []

    def read(self):
        """Reads and populates the trivia list."""
        with open(self.filename, "r") as f:
            blob = yaml.safe_load(f)
        self.trivia = blob["trivia"]
        self.fileread = True

    @property
    def select(self):
        """Returning a string assignment version (since __str__ is meant to be
        used with print and other methods.)"""
        if not self.fileread:
            self.read()
        return random.choice(self.trivia)

    def __str__(self):
        """Given a list of trivia facts, select one randomly and returns it so
        it may be printed."""
        if not self.fileread:
            self.read()
        return random.choice(self.trivia)


################################################################################
def main():
    """Main command line entry point"""
    parser = argparse.ArgumentParser(
        prog="bb_trivia", description="Prints out a random Blood Bowl trivia fact."
    )
    parser.add_argument("filename", help="The trivia data file (YAML format).")
    args = parser.parse_args()

    tfile = TriviaFile(args.filename)
    print(tfile)


################################################################################
if __name__ == "__main__":
    main()
