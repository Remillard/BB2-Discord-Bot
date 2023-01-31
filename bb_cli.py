#! python3
################################################################################
# Command line interface into the database
################################################################################
import os
import argparse

from sqlmodel import Session

import engine
import models

################################################################################
def main():
    bb_db_filename = "bb.db"
    my_engine = engine.initialize_db_and_tables(bb_db_filename)
    engine.initialize_enum_tables(my_engine)


if __name__ == "__main__":
    main()
