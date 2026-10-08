import argparse
import os
import re
import runpy
import sys
from pathlib import Path

# Inside the packaged .exe the step scripts are unpacked to sys._MEIPASS.
HERE = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
STEP_PATTERN = re.compile(r"^(\d+)_.+\.py$")


def find_steps():
    """Numbered scripts (1_xxx.py, 2_xxx.py, ...) as {number: path}, sorted by number."""
    steps = {}
    for path in HERE.glob("*.py"):
        match = STEP_PATTERN.match(path.name)
        if match:
            steps[int(match.group(1))] = path
    return dict(sorted(steps.items()))


def run_pipeline(source, output, numbers=None):
    """Run the given step numbers (default: all) in order."""
    os.environ["HW_SOURCE_FOLDER"] = source
    os.environ["HW_OUTPUT_FOLDER"] = output or source
    os.makedirs(os.environ["HW_OUTPUT_FOLDER"], exist_ok=True)

    available = find_steps()
    wanted = numbers or list(available)
    missing = [n for n in wanted if n not in available]
    if missing:
        raise ValueError(f"Unknown step number(s): {missing}. Available: {list(available)}")

    for number in wanted:
        path = available[number]
        print(f"Step {number}: {path.name}", flush=True)
        runpy.run_path(str(path), run_name="__main__")


def parse_args():
    parser = argparse.ArgumentParser(description="Run the numbered pipeline scripts in order")
    parser.add_argument("--input", required=True, help="source folder (.ist/.scn/.vmr folders, store_profile.xlsx)")
    parser.add_argument("--output", help="output folder (default: same as --input)")
    parser.add_argument("--steps", nargs="+", type=int, help="step numbers to run, in order (default: all)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        run_pipeline(args.input, args.output, args.steps)
    except ValueError as e:
        raise SystemExit(str(e))
