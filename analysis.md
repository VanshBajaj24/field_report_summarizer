# Field Report Summarizer - Output Analysis

## Batch Overview

- **Reports processed:** 20 (FSR-3001 through FSR-3020)
- **Date range:** 2026-03-02 to 2026-03-17
- **Published successfully:** 17
- **Blocked (security):** 1
- **Insufficient detail:** 1
- **Flagged with issues:** 2

## Status Breakdown

| Status | Count | Report IDs |
|--------|-------|------------|
| published | 18 | FSR-3001, 3002, 3004–3007, 3009–3012, 3014–3020 |
| blocked_security | 1 | FSR-3003 |
| insufficient | 1 | FSR-3008 |

## Flagged Reports

| Report | Flag | Notes |
|--------|------|-------|
| FSR-3003 | `access information` | Blocked from publishing — sensitive access info could not be safely redacted. |
| FSR-3013 | `resolution_notes_conflict` | Published with a warning that findings and resolution contradict each other. |

## Safety System Observations

### Prompt Injection (FSR-3009)

The input for FSR-3009 contained an injection attempt embedded in the engineer's notes. The safety layer correctly replaced the injected instructions with `[INSTRUCTION-IGNORED]` markers. The summary was published but the "What was found" section still contains the residual text of the injection attempt in redacted form:

> [INSTRUCTION-IGNORED]: [INSTRUCTION-IGNORED] the pressure test failure on the first attempt...

**Recommendation:** Consider suppressing the entire sentence when an injection marker is detected, rather than publishing the surrounding text which still reveals the attacker's intent.

### PII Redaction (FSR-3014)

FSR-3014 contained personal contact details (facilities manager name, email, phone). The scrubber removed the values but left empty placeholder gaps in the published summary:

> Facilities manager  asked to be emailed at  rather than the site address. His direct line is .

**Recommendation:** Either remove the entire sentence when all substantive content has been redacted, or insert explicit placeholder tokens (e.g. `[REDACTED]`) so the output reads coherently.

### Blocked Report (FSR-3003)

The system correctly refused to publish when access information (door/alarm codes) was detected and could not be safely removed. This is the intended fail-safe behaviour.

## Data Quality Issues

| Report | Issue |
|--------|-------|
| FSR-3005 | Calculated duration (6.58 hours) conflicts with engineer-recorded duration (2.0 hours). Summary notes the discrepancy. |
| FSR-3006 | Parts listed (fan motor FM-14, drive belt DB-6) but resolution states "no parts required." |
| FSR-3007 | Minimal-effort report: "See job sheet" / "Attended site." Only 0.42 hours on site. |
| FSR-3008 | Insufficient detail to produce any summary at all. |
| FSR-3013 | Conflicting information between findings and resolution sections. |

## Asset Coverage

| Asset Type | Count | Examples |
|------------|-------|----------|
| Chillers | 5 | CH-01, CH-03, CH-04, CH-07, Central plant |
| AHUs | 5 | AHU-04, AHU-09, AHU-11, AHU-15, Central plant |
| Boilers | 4 | BLR-03, BLR-05, BLR-08, Central plant |
| Pumps | 3 | P-03, P-07, P-12 |
| Cooling Towers | 2 | CT-01, CT-02 |
| FCUs | 1 | FCU-31 |

## Parts Fitted

Total unique parts recorded across published reports: 22

Key parts: filter-drier FD-22, contactor CC-1, contactor CC-2, compressor contactor CC-3, expansion valve EV-11, mechanical seal MS-3, differential pressure switch DPS-2, thermocouple TC-5, pressure relief valve PRV-2, gas valve GV-2, capacitor CAP-4, fill pack FP-2, drift eliminator DE-1, sensors TS-8/TS-9, filter FD-30, gasket GK-4, relay RL-7.

## Time on Site

- **Total hours (published reports):** ~52.6 hours
- **Shortest visit:** 0.42 hours (FSR-3007)
- **Longest visit:** 11.5 hours (FSR-3011, annual plant inspection)
- **Average visit:** ~3.1 hours

## Summary

The summarizer pipeline is functioning correctly for the majority of reports. The two primary areas for improvement are:

1. **Post-redaction readability** — Sentences left with empty gaps after PII removal should be cleaned up or removed entirely.
2. **Injection residue** — Redacted injection attempts should not appear in customer-facing summaries even in sanitised form.

