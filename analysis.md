# Field Report Summarizer - Output Analysis

## Batch Overview

- **Reports processed:** 20 (FSR-3001 through FSR-3020)
- **Date range:** 2026-03-02 to 2026-03-17
- **Published successfully:** 19
- **Insufficient detail:** 1
- **Flagged with issues:** 1

## Status Breakdown

| Status | Count | Report IDs |
|--------|-------|------------|
| published | 19 | FSR-3001–3007, 3009–3020 |
| insufficient | 1 | FSR-3008 |

## Flagged Reports

| Report | Flag | Notes |
|--------|------|-------|
| FSR-3013 | `resolution_notes_conflict` | Published with a warning that findings and resolution contradict each other. |

## Safety System Observations

### Physical Security Scrubbing (FSR-3003)

FSR-3003 contained a personal contact name, phone number, physical key location, and a plant room access code. The safety layer:

1. Removed entire sentences containing physical security information (spare key location and access code).
2. Redacted the remaining personal information (name and phone number).
3. Removed the redacted sentence because it contained only personal contact context with no maintenance content.

The report was published using fallback text for the findings section. The access code and key location do not appear in the published output.

### Prompt Injection (FSR-3009)

The input for FSR-3009 contained an injection attempt embedded in the engineer's notes. The safety layer detected the injection phrases and discarded the entire notes field, since injected text makes the whole field untrustworthy. The report was published using fallback text for the findings section.

### PII Redaction (FSR-3014)

FSR-3014 contained personal contact details (facilities manager name, email, phone). The safety layer redacted individual values and then removed the sentences entirely because they contained only personal contact context with no maintenance information. The report was published using fallback text for the findings section.

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

- **Total hours (published reports):** ~55.9 hours
- **Shortest visit:** 0.42 hours (FSR-3007)
- **Longest visit:** 11.5 hours (FSR-3011, annual plant inspection)
- **Average visit:** ~2.9 hours

## Summary

The summarizer pipeline processes all 20 reports correctly. The safety system:

1. **Classifies the kind of detail** rather than matching fixed phrases, covering physical access codes, key locations, security procedures, and access arrangements in any phrasing.
2. **Removes entire sentences** containing physical security information rather than token-replacing individual words.
3. **Discards all notes** when a prompt injection attempt is detected, since injected text makes the field untrustworthy.
4. **Removes sentences** left with only personal contact context after PII redaction rather than publishing empty gaps.
