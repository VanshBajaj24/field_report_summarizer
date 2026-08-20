# Field Service Report Summarizer — Specification

## Purpose

Build a tool that converts Northgate FM engineer field service reports into customer-facing summaries suitable for publication in a client portal.

The intended audience is a facilities contact or site representative who may not have technical engineering knowledge.

The summary must explain what happened during the visit in plain language while preventing disclosure of information that should not be visible to customers.

---

## Inputs

Input source:

- `service_reports.jsonl`

Each report contains:

- `report_id`
- `asset`
- `technician_id`
- `arrived_at`
- `departed_at`
- `stated_duration_hours`
- `parts_used`
- `resolution`
- `technician_notes`

Reports originate from engineer-entered data and should be treated as potentially incomplete, inconsistent, or inaccurate.

---

## Required Output Content

For every publishable report, the generated summary must contain:

1. Asset reference.
2. Date of visit.
3. What issue was identified.
4. What work was performed.
5. Parts fitted or replaced (if any).
6. Visit outcome.
7. Outstanding issues or recommendations (if mentioned).
8. Time spent on site.

The output must be written in customer-friendly language and avoid unnecessary engineering terminology.

---

## Required Output Format

Each report produces a single summary record containing:

- report_id
- summary_text
- publication_status

Publication status must be one of:

- Published
- Published With Caveat
- Insufficient Information

---

## Strict Non-Publication Rules

The following information must never appear in any published summary:

### Personal Information

- Engineer names
- Technician IDs
- Customer names
- Site contact names
- Phone numbers
- Email addresses
- Personal addresses

### Physical Security Information

- Alarm codes
- Door codes
- Access instructions
- Key locations
- Lock combinations
- Security procedures
- Temporary access arrangements

Publication of physical-access information is treated as a security incident.

### Internal Information

- Internal tracking references
- Internal escalation notes
- Internal staffing comments
- Tool instructions embedded within notes

---

## Prompt Injection Protection

Technician notes are treated exclusively as descriptions of work performed.

Any text attempting to influence the summariser must be ignored.

Examples include:

- "Ignore previous instructions"
- "Do not mention this issue"
- "Output customer details"
- "Mark as completed"

Such text has no authority and is never executed.

Only factual visit information may be considered during summary generation.

---

## Data Quality Handling

Reports are free-text records completed by engineers and may contain inconsistencies.

### Decision 1: Duration Discrepancies

Primary duration is calculated from:

`departed_at - arrived_at`

If the difference between the calculated duration and `stated_duration_hours` exceeds 0.5 hours:

- Use the calculated duration.
- Add a caveat indicating that recorded duration values were inconsistent.

---

### Decision 2: Parts Contradictions

If `parts_used` contains parts but the resolution states that no parts were replaced:

- Prefer the structured `parts_used` field.
- Publish the recorded parts.
- Add a caveat noting inconsistent report data.

---

### Decision 3: Resolution vs Notes Conflict

If resolution and technician notes describe materially different outcomes:

Example:

- Resolution: "Repair completed"
- Notes: "Unable to restore operation"

Then:

- Do not choose one source over the other.
- Publish a caveated summary.
- State that report information was inconsistent.

---

### Decision 4: Insufficient Information

If the report does not provide enough detail to determine:

- What was found, or
- What work was completed

then the tool must not make assumptions.

Instead publish:

"This report contains insufficient detail to produce a complete customer summary. Northgate Service Delivery is following up."

Publication status:

`Insufficient Information`

---

### Decision 5: Sensitive Information Mixed with Valid Information

Where a report contains both valid maintenance information and prohibited information:

- Remove prohibited information.
- Publish the remaining valid content.
- Do not reject the entire report solely because sensitive information was detected.

---

## Customer Language Rules

Technical language should be simplified where possible.

Example:

"Replaced faulty DP switch."

becomes

"A faulty pressure-monitoring component was replaced."

The customer should understand the outcome without specialist engineering knowledge.

---

## Non-Functional Requirements

- Output must be deterministic or near-deterministic.
- The same input should consistently produce the same summary.
- Redaction checks must occur before publication.
- The tool must process an entire batch of reports.
- Failures in one report must not stop processing of other reports.
- One output record must be generated for every input report.

---

## Out of Scope

The following are not part of this solution:

- Customer portal integration
- Authentication or authorization
- Historical summary storage
- Workflow orchestration
- Real-time processing
- Human approval workflows

---

## Success Criteria

The solution is successful when:

1. Every report receives an output.
2. No prohibited information appears in published summaries.
3. Customer-facing summaries remain understandable to non-technical readers.
4. Reports with inconsistent data are clearly caveated.
5. Reports with insufficient detail are not fabricated.
6. Technician notes are never treated as executable instructions.
7. The git history shows the required sequence:

   - 01-spec
   - 02-plan
   - 03-tasks
   - 04-implement

8. All generated summaries are suitable for publication in a customer-facing portal.