import re

PHONE_RE = re.compile(
    r"(?:\+?44\s?|0)(?:\d[\s-]?){9,10}",
    re.I,
)

EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

ACCESS_RE = re.compile(
    r"(?i)("
    # Security-context word followed by code-type word
    r"(?:door|alarm|access|entry|gate|building|keypad|intercom|"
    r"plant\s*room|security|lock|padlock|barrier|panel)\s*"
    r"(?:code|pin|number|combination|password|passcode)"
    r"|"
    # Code-type word followed by preposition + security-context word
    r"(?:code|pin|combination|password|passcode)\s+"
    r"(?:for|to|of)\s+(?:the\s+)?"
    r"(?:door|gate|building|plant\s*room|entrance|entry|lift|"
    r"elevator|car\s*park|parking|barrier|panel|room|premises|"
    r"site|lock|padlock|safe|cabinet)"
    r"|"
    # Standalone always-security terms
    r"\bpasscode\b|\bpassword\b|\bpin\s*(?:code|number)\b"
    r"|"
    # Code/pin/combination followed immediately by digits
    r"\b(?:code|pin|combination)\s*(?:is|:|=)\s*\d+"
    r"|"
    # Key storage and location patterns
    r"(?:spare|master|emergency|duplicate)\s*key"
    r"|"
    r"\bkey\s*(?:safe|box|location|cabinet|holder|hook|locker)\b"
    r"|"
    r"\bkey\s*(?:held|left|stored|kept|hidden|under|behind|with|at)\b"
    r"|"
    r"\blockbox\b|\block[\s-]*box\b"
    r"|"
    # Security procedures and access arrangements
    r"\bsecurity\s*(?:procedure|arrangement|instruction|protocol|detail)\b"
    r"|"
    r"\btemporary\s*access\b"
    r"|"
    r"\bout[\s-]*of[\s-]*hours\s*access\b"
    r"|"
    # Card/fob/badge access details
    r"(?:fob|badge|card|token)\s*(?:number|code|id|pin)"
    r")"
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


def _remove_security_sentences(text: str) -> str:
    parts = re.split(r'(?<=[.!?])\s+', text)
    clean = [p for p in parts if not ACCESS_RE.search(p)]
    return ' '.join(clean).strip()


def _clean_after_redaction(text: str) -> str:
    parts = re.split(r'(?<=[.!?])\s+', text)
    clean = []
    for p in parts:
        has_pii_context = NAME_HINT_RE.search(p)
        has_redaction = '[REDACTED-' in p
        if has_pii_context and has_redaction:
            continue
        clean.append(p)
    return ' '.join(clean).strip()


def scrub_notes(notes: str) -> str:
    if not notes:
        return ""

    text = notes

    if INJECTION_RE.search(text):
        return ""

    text = _remove_security_sentences(text)

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

    text = _clean_after_redaction(text)

    return text.strip()
