import re

from safety import (
    scrub_notes,
    PHONE_RE,
    EMAIL_RE,
    ACCESS_RE,
)

from quality import (
    actual_hours,
    duration_caveat,
    parts_note,
    is_insufficient,
    resolution_notes_conflict,
)


def build_summary(report):

    report_id = report.get("report_id")

    asset = report.get(
        "asset",
        "Unknown Asset"
    )

    resolution = (
        report.get("resolution") or ""
    ).strip()

    raw_notes = (
        report.get("technician_notes") or ""
    ).strip()

    notes = scrub_notes(raw_notes)

    parts = report.get("parts_used") or []

    arrival = report.get("arrived_at")
    departure = report.get("departed_at")

    visit_date = arrival[:10] if arrival else "Unknown"

    flags = []

    # Calculate duration safely
    try:
        actual = (
            actual_hours(arrival, departure)
            if arrival and departure
            else 0.0
        )

    except Exception:
        actual = 0.0
        flags.append("invalid_timestamp")

    # Detect resolution vs notes conflict
    if resolution_notes_conflict(
        resolution,
        notes
    ):
        flags.append(
            "resolution_notes_conflict"
        )

    # Handle insufficient information
    if is_insufficient(
        resolution,
        notes
    ):
        return {
            "report_id": report_id,
            "status": "insufficient",
            "summary": (
                "This report contains insufficient detail "
                "to produce a complete customer summary. "
                "Northgate Service Delivery is following up."
            ),
            "flags": flags,
        }

    # Remove redaction tokens before presenting notes
    clean_notes = re.sub(
        r"\[REDACTED-[^\]]+\]",
        "",
        notes,
    ).strip()

    found = (
        clean_notes
        if clean_notes
        else "Condition requiring attention was identified on arrival."
    )

    conflict_note = ""

    if "resolution_notes_conflict" in flags:
        conflict_note = (
            "The report contains conflicting information "
            "regarding the visit outcome and may require "
            "manual review."
        )

    summary = f"""
Asset: {asset}

Visit Date: {visit_date}

What was found:
{found}

What was done:
{resolution}

{parts_note(parts, resolution)}

Outstanding / Recommended:
{conflict_note or "None recorded for this visit."}

{duration_caveat(
    report.get("stated_duration_hours"),
    actual
)}
""".strip()

    # Post-generation safety validation.
    # Only block if truly sensitive information remains.

    security_residual = []

    if PHONE_RE.search(summary):
        security_residual.append(
            "phone number"
        )

    if EMAIL_RE.search(summary):
        security_residual.append(
            "email address"
        )

    if ACCESS_RE.search(summary):
        security_residual.append(
            "access information"
        )

    if security_residual:
        return {
            "report_id": report_id,
            "status": "blocked_security",
            "summary": (
                "A customer summary could not be published "
                "because sensitive information remained "
                "after processing."
            ),
            "flags": security_residual,
        }

    return {
        "report_id": report_id,
        "status": "published",
        "summary": summary,
        "flags": flags,
    }