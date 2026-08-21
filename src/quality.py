from datetime import datetime


def parse_ts(ts: str):
    return datetime.fromisoformat(ts)


def actual_hours(arrived: str, departed: str):

    duration = parse_ts(departed) - parse_ts(arrived)

    return round(
        duration.total_seconds() / 3600,
        2
    )


def duration_caveat(stated, actual):

    if stated is None:
        return f"Time on site: {actual} hours."

    if abs(actual - float(stated)) > 0.5:

        return (
            f"Time on site: {actual} hours "
            f"(calculated duration differs from "
            f"recorded duration of {stated} hours)."
        )

    return f"Time on site: {actual} hours."


def parts_note(parts, resolution):

    resolution = (resolution or "").lower()

    claims_no_parts = any(
        term in resolution
        for term in [
            "no parts",
            "inspection only",
            "no parts required"
        ]
    )

    if parts and claims_no_parts:

        return (
            f"Parts recorded: {', '.join(parts)}. "
            f"(Resolution states no parts required.)"
        )

    if parts:
        return f"Parts fitted: {', '.join(parts)}."

    return "No parts fitted."


def is_insufficient(resolution, notes):

    combined = f"{resolution} {notes}".strip()

    if len(combined) < 25:
        return True

    return False


def resolution_notes_conflict(
    resolution: str,
    notes: str,
) -> bool:

    resolution = (resolution or "").lower()
    notes = (notes or "").lower()

    positive_terms = [
        "repair completed",
        "resolved",
        "repaired",
        "restored",
        "alarm cleared",
        "completed"
    ]

    negative_terms = [
        "unable",
        "failed",
        "still faulty",
        "could not",
        "not restored",
        "requires further visit"
    ]

    resolution_positive = any(
        term in resolution
        for term in positive_terms
    )

    notes_negative = any(
        term in notes
        for term in negative_terms
    )

    return (
        resolution_positive
        and notes_negative
    )