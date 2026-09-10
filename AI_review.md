# AI Output Review

## Finding 1 — Security: Name Detection Too Narrow

**Issue:** The initial implementation only detected names when they appeared in specific phrases like "Site contact is John Smith."

**Risk:** Standalone personal names could be published.

**Code Change:** Added `POSSIBLE_NAME_RE` to detect any two-word capitalised name pattern and `scrub_notes` replaces matches with `[REDACTED-NAME]`. Post-generation validation is not affected because names are scrubbed before summary generation.

**Result:** Personal names are redacted regardless of surrounding context.

---

## Finding 2 — Reliability: Timestamp Parsing Failures

**Issue:** Timestamp parsing could fail on malformed records and stop summary generation.

**Code Change:** Wrapped the `actual_hours` call in `summarizer.py` with `try/except` and introduced an `invalid_timestamp` flag. A failed parse results in `actual = 0.0` and the flag is recorded on the report.

**Result:** The tool continues processing even when invalid timestamps are encountered.

---

## Finding 3 — Security: Withholding Rule Too Narrow

**Issue:** `ACCESS_RE` matched only five fixed phrases (`door code`, `alarm code`, `access code`, `spare key`, `key location`). A physical access detail phrased differently would pass through undetected.

**Risk:** Access codes, key locations, or security procedures could reach published summaries if worded in any way not covered by the five phrases.

**Code Change:** Rewrote `ACCESS_RE` in `safety.py` to classify the kind of detail rather than matching fixed phrases. The new regex covers:
- Security-context words (door, alarm, access, entry, gate, building, keypad, intercom, plant room, security, lock, padlock, barrier, panel) combined with code-type words (code, pin, number, combination, password, passcode).
- Reverse ordering: code-type word followed by a preposition and a security-context word (e.g. "code for the gate").
- Standalone always-security terms: passcode, password, pin code/number.
- Numeric code disclosure: code/pin/combination followed directly by digits.
- Key storage patterns: spare/master/emergency/duplicate key, key safe/box/location, key held/left/stored/kept/hidden.
- Security procedures and temporary access arrangements.
- Card/fob/badge/token access details.

Added `_remove_security_sentences` to remove entire sentences containing physical security information rather than token-replacing individual words.

**Result:** Physical security information is withheld regardless of phrasing. FSR-3003 is now published with the security sentences removed rather than blocking the entire report.

---

## Finding 4 — Readability: Injection Residue in Published Output

**Issue:** FSR-3009 contained a prompt injection attempt. The safety layer replaced the injection phrases with `[INSTRUCTION-IGNORED]` markers, but the surrounding text still appeared in the published summary, revealing the attacker's intent.

**Code Change:** Modified `scrub_notes` in `safety.py` to discard the entire notes field when an injection attempt is detected. Injected text makes the whole field untrustworthy, so no part of it should reach the output.

**Result:** FSR-3009 is published using fallback text. No residue of the injection attempt appears in the customer-facing summary.

---

## Finding 5 — Readability: Empty Gaps After PII Redaction

**Issue:** FSR-3014 contained personal contact details (name, email, phone). After PII values were replaced with redaction tokens and the tokens stripped, the published summary contained sentences with empty gaps: "Facilities manager asked to be emailed at rather than the site address."

**Code Change:** Added `_clean_after_redaction` in `safety.py` to remove sentences that contain both PII-context words (`site contact`, `facilities manager`, `direct line`, `mobile`) and redaction tokens, since those sentences have no maintenance content left.

**Result:** FSR-3014 is published using fallback text. No empty-gap sentences appear in the customer-facing summary.
