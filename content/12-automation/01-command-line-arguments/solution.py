import argparse
import sys


def build_parser():
    parser = argparse.ArgumentParser(description="Show the first lines of a file.")
    parser.add_argument("path")
    parser.add_argument("-n", "--limit", type=int, default=5)
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        with open(args.path) as file:
            lines = file.read().splitlines()[: args.limit]
    except FileNotFoundError:
        print(f"error: no such file: {args.path}", file=sys.stderr)
        return 1
    if args.verbose:
        print(f"Reading {args.path}")
    for line in lines:
        print(line)
    return 0
