# Write two functions:
#
# def parse_requirements(text): ...     "requests==2.31.0\nflask >= 2.0\nnumpy" ->
#                                        [("requests", "==2.31.0"), ("flask", ">=2.0"), ("numpy", "")]
# def requirements_text(versions): ...   {"b": "1.0", "a": None} -> "a\nb==1.0\n"
