import argparse
from pathlib import Path

from loader import load_reports
from summarizer import build_summary
from writer import write_outputs


def main():

    parser = argparse.ArgumentParser(
        description="Field Service Report Summarizer"
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=Path(
            "data/service_reports.jsonl"
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs"),
    )

    args = parser.parse_args()

    reports = load_reports(
        args.input
    )

    results = []

    for report in reports:
        results.append(
            build_summary(report)
        )

    write_outputs(
        results,
        args.output
    )

    published = sum(
        1
        for r in results
        if r["status"] == "published"
    )

    print(
        f"Processed {len(results)} reports "
        f"→ {published} published, "
        f"{len(results)-published} flagged."
    )


if __name__ == "__main__":
    main()