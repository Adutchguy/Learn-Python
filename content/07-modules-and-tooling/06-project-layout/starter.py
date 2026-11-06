# Write two functions (use pathlib.Path):
#
# def package_name(project_name): ...      "My Cool-Tool" -> "my_cool_tool"
# def scaffold_project(root, name): ...    create root/name with README.md, pyproject.toml,
#                                          src/PACKAGE/__init__.py and tests/test_smoke.py;
#                                          return the project Path; FileExistsError if it exists
