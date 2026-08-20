# Tasks — Field Service Report Summarizer

## Objective

Implement the solution defined in `spec.md` using the architecture described in `plan.md`.

---

## Task 1 – Load and Parse Reports

### Goal

Read all reports from the JSONL input file.

### Actions

- Read the input file line by line.
- Parse each JSON object.
- Validate required fields are present.
- Handle malformed records gracefully.
- Continue processing remaining reports if one record fails.

### Done When

- All valid reports are loaded successfully.
- Invalid records are flagged without stopping the batch.

---

## Task 2 – Implement Safety Detection

### Goal

Identify information that must never appear in customer-facing summaries.

### Actions

- Detect phone numbers.
- Detect email addresses.
- Detect technician IDs.
- Detect personal names and contact references.
- Detect access codes.
- Detect alarm codes.
- Detect key locations.
- Detect physical access instructions.
- Detect prompt-injection phrases.

### Done When

- Sensitive content can be detected before summary generation.

---

## Task 3 – Implement Note Sanitisation

### Goal

Ensure prohibited content never reaches published output.

### Actions

- Replace phone numbers with redaction tokens.
- Replace email addresses with redaction tokens.
- Replace names where appropriate.
- Remove access codes and security details.
- Remove prompt-injection instructions.
- Preserve useful maintenance information where possible.

### Done When

- Sanitised notes contain only customer-safe information.

---

## Task 4 – Calculate Visit Duration

### Goal

Generate accurate customer-facing time-on-site information.

### Actions

- Calculate duration from arrival and departure timestamps.
- Compare against stated duration.
- Detect discrepancies greater than the specification threshold.
- Generate duration caveats where required.

### Done When

- Duration information is available for every valid report.

---

## Task 5 – Detect Report Inconsistencies

### Goal

Surface data-quality issues instead of silently resolving them.

### Actions

#### Duration Mismatch

- Compare calculated and stated duration.

#### Parts Contradiction

- Detect reports where parts are recorded but resolution claims no parts were used.

#### Resolution vs Notes Conflict

- Detect reports where repair outcome described in notes conflicts with resolution text.

### Done When

- Contradictions are flagged and included in output status.

---

## Task 6 – Detect Insufficient Information

### Goal

Prevent creation of misleading summaries.

### Actions

- Evaluate available information.
- Determine whether:
  - What was found
  - What was done

can be reliably described.

### Done When

- Reports lacking sufficient detail use the approved follow-up message.

---

## Task 7 – Generate Customer-Facing Summaries

### Goal

Create summaries that facilities contacts can easily understand.

### Actions

Generate:

- Asset reference
- Visit date
- What was found
- What was done
- Parts fitted
- Outstanding recommendations
- Time on site

### Rules

- Use plain language.
- Do not invent facts.
- Prefer structured data where conflicts exist.
- Include caveats where required.

### Done When

- Every report produces a summary or approved fallback message.

---

## Task 8 – Implement Publication Status Logic

### Goal

Assign an appropriate publication outcome.

### Actions

Support:

- Published
- Published With Caveat
- Insufficient Information
- Blocked for Security Review

### Done When

- Every report receives a publication status.

---

## Task 9 – Implement Post-Generation Validation

### Goal

Verify generated summaries remain safe after generation.

### Actions

- Re-scan generated summaries.
- Check for:
  - Names
  - Phone numbers
  - Emails
  - Technician IDs
  - Access information
  - Security information

### Done When

- Unsafe summaries are blocked before publication.

---

## Task 10 – Generate Outputs

### Goal

Produce required deliverables.

### Actions

- Create one Markdown file per report.
- Create combined JSON output.
- Include:
  - report_id
  - publication_status
  - summary
  - flags

### Done When

- Outputs exist for every processed report.

---

## Task 11 – Automated Testing

### Goal

Verify specification compliance.

### Test Cases

- Normal report
- Duration mismatch
- Parts contradiction
- Resolution conflict
- Insufficient information
- Prompt injection attempt
- Phone number redaction
- Email redaction
- Access code redaction
- Physical security information
- Post-generation validation

### Done When

- All critical scenarios are covered.

---

## Task 12 – Dataset Verification

### Goal

Validate behaviour against the supplied reports.

### Actions

- Run all 20 reports.
- Manually review every output.
- Verify:
  - No sensitive information leaked.
  - Caveats are correct.
  - Contradictions are surfaced.
  - Insufficient-information reports use approved wording.

### Done When

- Outputs satisfy the specification.

---

## Task 13 – AI Output Review

### Goal

Review AI-assisted implementation before submission.

### Review Areas

#### Intent

- Does the implementation satisfy the specification?

#### Tests

- Are important cases covered?

#### Security

- Can prohibited information reach publication?

#### Performance

- Can all reports be processed efficiently?

#### Maintainability

- Is the code understandable and easy to modify?

### Deliverables

- Review document.
- At least one real issue identified.
- Evidence of correction.

### Done When

- Review findings are documented and fixes applied.

---

## Final Submission Checklist

- [ ] Spec committed as `01-spec`
- [ ] Plan committed as `02-plan`
- [ ] Tasks committed as `03-tasks`
- [ ] Implementation committed as `04-implement`
- [ ] All reports processed
- [ ] No prohibited information published
- [ ] Inconsistencies surfaced correctly
- [ ] Insufficient-information reports handled correctly
- [ ] AI review completed
- [ ] Deliverables prepared for submission