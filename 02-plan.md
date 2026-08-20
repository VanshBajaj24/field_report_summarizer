# Plan — Field Service Report Summarizer

## Approach

### 1. Spec-first (already done)

The specification defines:

- Required customer-facing content.
- Absolute non-publication rules.
- Handling of conflicting report fields.
- Handling of insufficient-information reports.
- Prompt-injection protection rules.

The implementation will treat the specification as the source of truth.

---

### 2. Architecture

- Small Python CLI / batch processor.
- Input: path to a JSONL file of reports.
- Output:
  - Directory of Markdown summaries (one file per report)
  - Combined JSON index of results

Core processing pipeline:

a. Load and parse reports.

b. Safety scan:
   - Detect technician IDs
   - Detect phone numbers
   - Detect email addresses
   - Detect access codes
   - Detect alarm codes
   - Detect physical access instructions
   - Detect personal information
   - Detect prompt-injection attempts

c. Duration calculation and consistency checks.

d. Report quality checks:
   - Duration mismatch detection
   - Parts-versus-resolution contradiction detection
   - Resolution-versus-notes contradiction detection
   - Insufficient-information detection

e. Sanitise technician notes by removing or replacing prohibited content.

f. Generate customer-facing summaries using deterministic templates.

g. Post-generation validation:
   - Re-scan generated summaries.
   - Verify no prohibited information remains.
   - Block publication if sensitive information is still detected.

h. Write outputs.

---

### 3. Summary Generation Strategy

Primary approach:

- Deterministic template-based summary generation.

The summariser will construct customer-facing summaries from structured report fields and sanitised notes.

Reasons for this approach:

- Predictable behaviour.
- Easier testing.
- Stronger control over customer-visible content.
- Reduced risk of privacy or security information appearing in summaries.

Required sections:

- Asset reference
- Visit date
- What was found
- What was done
- Parts fitted
- Outstanding or recommended actions
- Time on site

No information will be invented.

---

### 4. Publication Status Strategy

Each report receives one of the following statuses.

#### Published

The report contains sufficient information and no blocking issues.

#### Published With Caveat

The report contains:

- Duration discrepancies
- Contradictory fields
- Data-quality concerns

The summary includes an explanation of the issue.

#### Insufficient Information

The report lacks sufficient detail to determine:

- What was found
- What was done

The approved follow-up message from the specification is published instead.

#### Blocked for Security Review

Sensitive information remains after processing and cannot be safely removed.

The summary is withheld and flagged for review.

---

### 5. Safety Strategy (Defence in Depth)

Customer-facing safety takes priority over completeness.

#### Pre-Generation Filtering

Before summary generation:

- Detect personal information.
- Detect contact information.
- Detect physical-security information.
- Detect prompt-injection attempts.

Sensitive material is removed or replaced with redaction tokens.

#### Prompt-Injection Protection

Technician notes are treated solely as descriptions of the visit.

Any statements attempting to:

- Change behaviour
- Influence output
- Override rules
- Hide information

are ignored.

#### Post-Generation Validation

Generated summaries are scanned again.

Checks include:

- Personal information
- Contact information
- Access instructions
- Alarm or access codes
- Residual security-sensitive content

Publication is blocked if prohibited information remains.

---

### 6. Data Quality Strategy

The implementation applies the decisions recorded in the specification.

#### Duration Mismatch

- Calculate duration from arrival and departure timestamps.
- Compare to stated duration.
- Use calculated duration.
- Include caveat when discrepancy exceeds threshold.

#### Parts Contradiction

- Prefer the structured `parts_used` field.
- Include caveat describing the inconsistency.

#### Resolution vs Notes Conflict

- Detect conflicting outcomes.
- Do not resolve automatically.
- Publish with caveat.

#### Insufficient Detail

- Do not invent missing information.
- Publish approved follow-up message.

#### Mixed Safe and Sensitive Content

- Remove sensitive content.
- Retain safe maintenance information where possible.

---

### 7. Error Handling Strategy

The batch must continue processing if a single report fails.

Approach:

- Validate each report independently.
- Record processing issues.
- Continue processing remaining reports.
- Produce outputs for all recoverable reports.

Malformed timestamps and missing fields will be handled gracefully and reported.

---

### 8. Testing Strategy

#### Automated Tests

Cover:

- Valid report
- Duration mismatch
- Parts contradiction
- Resolution conflict
- Insufficient information
- Name detection
- Email detection
- Phone number detection
- Access-code detection
- Prompt-injection attempts
- Post-generation safety validation

#### Dataset Validation

Run against all 20 supplied reports.

Verification checklist:

- No names leaked
- No technician IDs leaked
- No phone numbers leaked
- No email addresses leaked
- No access instructions leaked
- No access codes leaked
- No alarm codes leaked
- Duration caveats applied correctly
- Contradictions surfaced correctly
- Insufficient-information reports handled correctly

---

### 9. Git Discipline

Required commit sequence:

1. 01-spec
2. 02-plan
3. 03-tasks
4. 04-implement

No source files will be introduced before the implementation commit.

Git history serves as evidence of Spec-Driven Development.

---

### 10. AI Usage and Review

AI may be used during implementation but all generated code will be reviewed before submission.

Review areas:

- Intent
- Tests
- Security
- Performance
- Maintainability

At least one genuine issue will be identified, corrected, and documented.

The review will assess both:

- Implementation quality
- Customer-facing output safety

---

### 11. Deliverables After Implementation

- Working summarisation tool.
- Markdown summaries for all reports.
- Combined JSON output.
- Analysis of problematic reports.
- AI review findings and corrections.
- Documentation of specification decisions.
- Git history demonstrating the required commit sequence.
- Demo notes.
- Declared-effort statement.