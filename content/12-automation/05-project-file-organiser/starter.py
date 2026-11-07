import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    # fill in: suffix -> category, for example ".jpg": "Images"
}


# Write five functions:
#
# def category_for(filename): ...           "Images", "Documents", "Archives" or "Other"
# def unique_destination(path): ...         path, or "name (1).ext", "name (2).ext" ... if it exists
# def plan_moves(folder): ...               [(source, destination)] for the files directly in folder, sorted by name
# def organise(folder, dry_run=False): ...  do the moves; return ["cat.jpg -> Images", ...]
# def main(argv=None): ...                  --dry-run flag, print the lines and a summary, return 0
