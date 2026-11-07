import shutil
from pathlib import Path


# Write four functions:
#
# def files_by_extension(folder): ...         {".txt": ["a.txt", "b.txt"], "": ["README"]}, files directly in folder
# def big_files(folder, min_bytes): ...       sorted relative paths of files (in subfolders too) of at least min_bytes
# def total_size(folder): ...                 total bytes of every file in the folder and its subfolders
# def copy_matching(src, dst, extension): ... copy the files in src with that extension into dst; sorted names
