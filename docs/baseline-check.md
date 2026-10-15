# Baseline Check — CampusFlow Next

**Date:** 2026-10-15
**Engineer:** Elizabeth Odeh
**Commit:** 94938ba

## Run command

python3 main.py

## Test command

python3 -m unittest discover -s tests -v

## Test results

Ran 34 tests in 0.059s
Result: OK — all 34 tests passed.

Test coverage by module:
- test_reports.py — 4 tests (work queue, report counts, empty case)
- test_storage.py — 4 tests (corrupt JSON, ID uniqueness, missing file, save/reload)
- test_tickets.py — 14 tests (priority rules, validation)
- test_validation.py — 4 tests (affected_users validation)
- test_workflow.py — 8 tests (transitions, reopen, assignment)

## Three inputs I tested manually

1. Ran `python3 main.py` → menu displayed correctly with 9 options.
2. Typed an invalid choice (multi-character paste) → app printed "Invalid choice. Please enter a number between 1 and 9." and re-prompted. App did NOT crash.
3. [add one more if you tried it — otherwise say "not tested"]

## What my audit said needed improvement

[Paste the exact audit findings here. If you don't have them, write:
"The audit was not available at the time of writing. Based on the project brief, the expected improvements are: validation hardening (bool rejection), structured notes, combined search filters, enhanced reports, and safe JSON validation."]

## What I noticed

- The app already passes 34 tests — good starting point.
- `validation.py` already exists but is small (482 bytes).
- No `notes.py`, `search.py`, `understanding_check.py` yet.
- Menu redraws over itself when invalid input is pasted, but doesn't crash.

## What I plan to add

- Strengthen `validation.py` with bool rejection for `affected_users`.
- Add tests for the bool trap.
- Document contracts for new functions.