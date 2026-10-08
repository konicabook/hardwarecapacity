import os
import sys

# main.py / app.py set these env vars; the default lets a step run on its own.
_DEFAULT_SOURCE = r"D:\ITH\tempdownload\ca\202609"


def source_folder():
    return os.environ.get("HW_SOURCE_FOLDER", _DEFAULT_SOURCE)


def output_folder():
    return os.environ.get("HW_OUTPUT_FOLDER", source_folder())


def src(*parts):
    return os.path.join(source_folder(), *parts)


def out(*parts):
    return os.path.join(output_folder(), *parts)


def resource(name):
    """Bundled data file (POS_Model.csv, ...): next to the code, or inside the .exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)
