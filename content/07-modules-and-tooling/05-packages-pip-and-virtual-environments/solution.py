import re


def parse_requirements(text):
    packages = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        name = re.match(r"[A-Za-z0-9][A-Za-z0-9._-]*", line).group(0)
        spec = line[len(name):].replace(" ", "")
        packages.append((name, spec))
    return packages


def requirements_text(versions):
    text = ""
    for name in sorted(versions):
        version = versions[name]
        text += f"{name}=={version}\n" if version else f"{name}\n"
    return text
