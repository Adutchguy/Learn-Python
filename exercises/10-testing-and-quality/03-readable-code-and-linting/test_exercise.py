def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


import ast
import linecache
import re


def _source():
    import exercise

    return "".join(linecache.getlines(exercise.__file__))


def _tree():
    return ast.parse(_source())


def test_functions_were_renamed_and_still_work():
    calculate_total = _fn("calculate_total")
    is_valid_email = _fn("is_valid_email")
    read_number = _fn("read_number")
    assert calculate_total([10, 20]) == 33.0, f"calculate_total([10, 20]) should be 33.0 (30 plus 10% tax), got {calculate_total([10, 20])!r}"
    assert calculate_total([10, 20], 0.0, [5]) == 25.0, "discounts should be subtracted before tax"
    assert calculate_total([100], tax_rate=0.2, discounts=None) == 120.0, "discounts=None should be allowed"
    assert is_valid_email("ada@example.com") is True, "ada@example.com is valid"
    assert is_valid_email("ada@example") is False, "no dot after the @ means invalid"
    assert is_valid_email("@example.com") is False, "nothing before the @ means invalid"
    assert is_valid_email("a@b@c.com") is False, "two @ signs means invalid"
    assert read_number("42") == 42 and read_number("x") is None, "read_number should return an int, or None for bad text"


def test_constant_is_named_in_upper_case():
    import exercise

    assert getattr(exercise, "MAX_ITEMS", None) == 10, "Rename maxItems to MAX_ITEMS (still equal to 10)"
    assert not hasattr(exercise, "maxItems"), "The old name maxItems should be gone"


def test_calculate_total_does_not_share_a_default_list():
    import inspect

    calculate_total = _fn("calculate_total")
    defaults = [p.default for p in inspect.signature(calculate_total).parameters.values()]
    assert not any(isinstance(d, (list, dict, set)) for d in defaults), "Do not use a list, dict or set as a default argument: use None and create the list inside"


def test_no_unused_imports():
    tree = _tree()
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported[(alias.asname or alias.name).split(".")[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported[alias.asname or alias.name] = node.lineno
    used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    unused = sorted(name for name in imported if name not in used)
    assert not unused, f"These imports are never used, so remove them: {unused}"


def test_one_import_per_line():
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            assert len(node.names) == 1, f"Line {node.lineno}: put each import on its own line instead of 'import a, b'"


def test_names_follow_pep8():
    for node in ast.walk(_tree()):
        if isinstance(node, ast.FunctionDef):
            assert re.fullmatch(r"[a-z_][a-z0-9_]*", node.name), f"Function name {node.name!r} should be snake_case (lowercase with underscores)"
            for arg in node.args.args:
                assert re.fullmatch(r"[a-z_][a-z0-9_]*", arg.arg), f"Parameter name {arg.arg!r} should be snake_case"


def test_every_function_has_a_docstring():
    for node in ast.walk(_tree()):
        if isinstance(node, ast.FunctionDef):
            assert ast.get_docstring(node), f"Function {node.name} needs a docstring: a string on the line right under def"


def test_no_bare_except_and_no_comparison_to_none():
    for node in ast.walk(_tree()):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, f"Line {node.lineno}: a bare 'except:' hides every error. Name the error, for example 'except ValueError:'"
        if isinstance(node, ast.Compare):
            for op, right in zip(node.ops, node.comparators):
                if isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(right, ast.Constant) and right.value is None:
                    raise AssertionError(f"Line {node.lineno}: compare with None using 'is None' / 'is not None'")


def test_layout_rules():
    source = _source()
    for number, line in enumerate(source.splitlines(), 1):
        assert "\t" not in line, f"Line {number}: use 4 spaces, not tab characters"
        assert line == line.rstrip(), f"Line {number}: remove the spaces at the end of the line"
        assert len(line) <= 79, f"Line {number} is {len(line)} characters long; keep lines to 79 or fewer"


def test_spaces_around_assignment():
    source = _source()
    assert not re.search(r"^[A-Za-z_]\w*=\S", source, re.M), "Put spaces around = in assignments, like MAX_ITEMS = 10"
    assert "==" not in source.replace(" == ", ""), "Put a space on both sides of == (and other operators)"
