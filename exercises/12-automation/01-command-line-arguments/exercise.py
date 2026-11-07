import argparse
import sys


# Write two functions:
#
# def build_parser(): ...     path (positional), -n/--limit (int, default 5), -v/--verbose (flag)
# def main(argv=None): ...    print the first `limit` lines of the file; return 0, or 1 if the file is missing
