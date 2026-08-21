import re

PHONE_RE = re.compile(
    r"(?:\+?44\s?|0)(?:\d[\s-]?){9,10}",
    re.I,
)

EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

ACCESS_RE = re.compile(
    r"(?i)(door code|alarm code|access code|spare key|key location)"
)

INJECTION_RE = re.compile(
    r"(?i)(important instruction for the summary tool|ignore previous instructions|do not mention)"
)

NAME_HINT_RE = re.compile(
    r"(?i)(site contact|facilities manager|direct line|mobile)"
)

POSSIBLE_NAME_RE = re.compile(
    r"\b[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\b"
)


def contains_forbidden(text: str) -> list[str]:
    if not text:
        return []

    reasons = []

    if PHONE_RE.search(text):
        reasons.append("phone number")

    if EMAIL_RE.search(text):
        reasons.append("email address")

    if ACCESS_RE.search(text):
        reasons.append("access information")

    if NAME_HINT_RE.search(text):
        reasons.append("personal contact information")

    if POSSIBLE_NAME_RE.search(text):
        reasons.append("possible personal name")

    if INJECTION_RE.search(text):
        reasons.append("prompt injection attempt")

    return reasons


def scrub_notes(notes: str) -> str:
    if not notes:
        return ""

    text = notes

    text = PHONE_RE.sub(
        "[REDACTED-PHONE]",
        text
    )

    text = EMAIL_RE.sub(
        "[REDACTED-EMAIL]",
        text
    )

    text = POSSIBLE_NAME_RE.sub(
        "[REDACTED-NAME]",
        text
    )

    text = re.sub(
        r"(?i)(site\s*contact\s*is\s*)[A-Za-z][A-Za-z\s\-']+",
        r"\1[REDACTED-NAME]",
        text,
    )

    text = re.sub(
        r"(?i)(facilities\s*manager\s*)[A-Za-z][A-Za-z\s\-']+",
        r"\1[REDACTED-NAME]",
        text,
    )

    text = re.sub(
        r"(?i)(access\s*code\s*is\s*)\d+",
        r"\1[REDACTED-CODE]",
        text,
    )

    text = INJECTION_RE.sub(
        "[INSTRUCTION-IGNORED]",
        text,
    )

    return text.strip()