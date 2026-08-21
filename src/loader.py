import json
from pathlib import Path


def load_reports(input_file: Path):
    reports = []

    with input_file.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                reports.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"Invalid JSON on line {line_no}")

    return reports