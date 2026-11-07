import subprocess
import sys


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout


def python_version():
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    return result.stdout.strip()


def run_or_none(command, timeout):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    return result.stdout.strip()


def echo_safely(text):
    code = "import sys; print(sys.argv[1])"
    result = subprocess.run([sys.executable, "-c", code, text], capture_output=True, text=True)
    return result.stdout.strip()
