import json
from pathlib import Path


def write_outputs(results, output_dir: Path):

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for result in results:

        output_file = (
            output_dir
            / f"{result['report_id']}.md"
        )

        output_file.write_text(
            result["summary"],
            encoding="utf-8"
        )

    index_file = (
        output_dir
        / "summaries.json"
    )

    index_file.write_text(
        json.dumps(
            results,
            indent=2
        ),
        encoding="utf-8",
    )