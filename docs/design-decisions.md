# Design Decisions — CampusFlow CLI

## 1. Team Ownership & Role Distribution

In alignment with **PRD Section 11** and the agreed sprint roles:

- **Engineer A: Alexander Agbaji (@AgbajiAlexander) — Upstream / Core Data & Persistence**:
  - **F1 — Create Ticket**: Input validation, ID sequencing (`T001`), and priority evaluation.
  - **F2 — List & View**: Tabular summaries and full record lookups.
  - **F7 — Persistence**: Safe JSON storage, atomic file replacement, and corruption protection.
  - **Branch**: `feat/1-core-ticket-storage`
  - **Repository**: Upstream central repository (`https://github.com/AgbajiAlexander/CampusFlow.git`).

- **Engineer B: Eli Odeh (@eliodeh) — Fork / Workflow & Analytics**:
  - **F3 — Assign Staff**: Assignee validation and reassignment handling.
  - **F4 — Ticket Lifecycle**: State machine transitions (`open -> in_progress -> resolved`) and resolved-ticket locking / reopening.
  - **F5 — Work Queue**: Filtered active ticket prioritization with numeric ID tie-breakers.
  - **F6 — Analytical Reports**: Summary counts and status/priority aggregations with zero-count safety.
  - **CLI Menu Loop**: Interactive console driver integrating all modules.
  - **Branch**: `feat/2-workflow-reporting`
  - **Repository**: Developer fork (`https://github.com/eliodeh/CampusFlow.git`).

---

## 2. Architecture & Modular Separation of Concerns

The application adheres to clean separation of concerns without external third-party dependencies (Python standard library only):

```
CampusFlowTeamG/
├── tickets.py          # Data validation, normalization, ID sequencing, Priority Engine
├── storage.py          # JSON read/write, atomic replacement, corruption handling
├── workflow.py         # Assignment logic, state transitions, locking, reopening
├── reports.py          # Work queue filtering/sorting, volume reports
├── cli.py              # Interactive console interface and input loop
├── main.py             # Application entrypoint
├── tests/              # Modular unittest test suites (30 tests)
│   ├── test_tickets.py
│   ├── test_workflow.py
│   ├── test_storage.py
│   └── test_reports.py
├── docs/               # Sprint governance, AI learning logs, and PR reviews
│   ├── design-decisions.md
│   ├── ai-learning-log.md
│   └── pr-reviews.md
├── data/               # Local runtime data directory (ignored in git)
└── PRD.md              # Product Requirement Document
```

---

## 3. Data Model & Input Normalization Decisions

1. **Identifier Format (`id`)**:
   - Sequential format `T001`, `T002`, `T003`...
   - Extracted numerically on reload so subsequent ticket creations never collide, even after deleting or modifying previous tickets.

2. **Case Normalization**:
   - `category`: Accepted case-insensitively and stored strictly normalized as `Network`, `Hardware`, `Software`, or `Other`.
   - `urgency`: Accepted case-insensitively and stored normalized as lowercase (`low`, `medium`, `high`).
   - `status`: Normalizes to lowercase (`open`, `in_progress`, `resolved`).
   - `affected_users`: Must strictly be a positive integer > 0. Floating-point numbers, negative numbers, 0, and non-numeric text are explicitly rejected with distinct error messages.

3. **Pure Priority Engine**:
   - `calculate_priority(urgency, affected_users)` is implemented as a pure function without I/O or global state, allowing 100% deterministic unit testing against PRD Section 7 rules.

---

## 4. Lifecycle & State Machine Security

- **Unassigned Gate**: A ticket with `assigned_to = None` CANNOT move to `in_progress`.
- **Lock on Resolved**: Once a ticket reaches `resolved`, it cannot directly transition to any other status.
- **Explicit Reopen**: A resolved ticket can only be modified if explicitly reopened via `reopen_ticket`, resetting its status to `open`.
- **Atomic Operations**: Any invalid transition raises a `ValueError` without mutating stored ticket attributes.

---

## 5. Storage & Persistence Reliability

- **Persistence Timing**: In addition to saving upon clean exit, CampusFlow automatically persists tickets immediately after every state mutation (create, assign, transition, reopen). This eliminates data loss in unexpected terminal disconnections.
- **Corrupt Storage Defense**: If `data/tickets.json` contains malformed or corrupted JSON, `storage.load_tickets` returns a descriptive error message and an empty in-memory list **without** truncating or overwriting the damaged file on disk.
- **Atomic Writes**: Saves write first to a `.tmp` file and perform an atomic filesystem replacement (`os.replace`) to prevent corrupted half-written files during sudden process termination.

---

## 6. GitHub Multi-Repo Collaboration Workflow

To reflect the team's two-repository setup:
1. `origin`: Upstream repository managed by Engineer A — Alexander Agbaji (`https://github.com/AgbajiAlexander/CampusFlow.git`).
2. `fork`: Forked repository managed by Engineer B — Eli Odeh (`https://github.com/eliodeh/CampusFlow.git`).
3. Branches follow the required specification: `<type>/<issue-number>-<short-description>`.
4. Pull Requests require cross-engineer reviews with substantive technical comments prior to merging into `main`.




# AI Learning Log: Engineer A (Ticket Safety & Storage)

## Cycle 1: Side effects and function contracts
**What I asked:** I said I didn't know what a side effect was and asked the AI to explain it.
**What confused me:** I first described a side effect as "anything a function does outside its body." The AI corrected me: a side effect is any change that happens besides the answer the function returns.
**What I understand now:** Printing, saving a file, and changing a dictionary are side effects. If a function's contract doesn't mention them, it must not do them. For example, if `add_note` printed "Note saved!" and B's CLI also printed "Note added.", the user would see two messages and B would lose control of the output.

## Cycle 2: Validate-before-mutate
**What I asked:** I was given a `transition_ticket` example that changed the status before checking `assigned_to`.
**What I understand now:** A function that can fail must change nothing on failure. All checks come first, and the change happens last.
**Still shaky:** I can say the rule, but I had trouble explaining why it applies to every function.

## Cycle 3: The boolean trap
**What I asked:** I was asked what happens when `validate_affected_users(True)` is called.
**What I understand now:** In Python, `bool` is a subtype of `int`, so `isinstance(True, int)` is `True` and `True` passes a naive check. The bool check must come before the int check. If `True` is stored, the system doesn't crash. It silently produces wrong data.
**What I got wrong first:** I put the bool check "after" the int check and gave answers that didn't match the question. It took several retries.

## Cycle 4: Atomic load, max + 1, and note IDs
**What I was taught:** `load_tickets` builds a new list and returns it only if every record passes, so a failed load leaves current memory unchanged. Next IDs come from the highest existing ID + 1, not the count + 1. `add_note` validates before generating an ID, so a failed call consumes no ID.
**Honest status:** I got Q4 to Q8 wrong on my first attempt and was shown the correct answers. I have not yet shown that I can produce them on my own.

## Cycle 5: Writing contracts
I wrote contracts for `validate_affected_users`, `add_note`, `get_notes` and `transition_ticket`. I made mistakes on most of them because I copied the previous contract instead of reading the function name and parentheses. The final versions are in `docs/design-decisions.md`.

## Not completed
- Baseline check (`baseline-check.md`)
- Code for validation, notes, transitions, and JSON load/save
- Tests
- Peer review and pull requests

**Reason:** I started with limited time and was still learning the underlying concepts (side effects, validate-before-mutate, atomic load). I plan to continue with the code in the next session.

## What I would do next
1. I Re-answered  Q4 to Q8 from memory without help.
2. Write `validate_affected_users` with the bool check first.
3. Write tests for `True`, `False`, `0`, `-3` and `5`.





# Design Decisions — CampusFlow Next

**Engineer:** Engineer A (Ticket Safety & Storage)
**Date:** 2026-10-15

This document records the key engineering decisions behind CampusFlow Next's data layer. Each decision explains *why* the approach was chosen, not just *what* it does.

---

## ADR-001: Exceptions over return values for validation

**Date:** 2026-10-15
**Status:** Accepted

### Context
Engineer B's CLI calls Engineer A's validation and mutation functions. We need a consistent way to signal failure. Two options: return a special value (like `None` or a tuple), or raise an exception.

### Decision
Use typed exceptions: `ValidationError`, `NoteError`, `StorageError`, `TransitionError`. All validation and mutation functions raise these on failure.

### Consequences
- B's CLI wraps every call in `try/except`.
- Business logic stays clean — no need to check for `None` after every call.
- Exception types are meaningful and can be caught specifically.

### Alternatives considered
**Result tuples** (`(ok, error)`) were rejected because callers can forget to check them. Exceptions cannot be ignored silently.

---

## ADR-002: Validate-before-mutate

**Date:** 2026-10-15
**Status:** Accepted

### Context
If a function validates *after* mutating, a failed validation leaves data in a corrupted state. The brief requires: *"Invalid actions must leave the entire ticket collection unchanged."*

### Decision
Every mutation function follows this order:
1. Validate all preconditions.
2. If all pass, mutate.
3. If any fail, raise without touching data.

### Consequences
- Rejected actions leave the collection byte-for-byte identical.
- Tests can snapshot state before an action and compare it after a rejection.
- The invariant is: **a function that can fail must change nothing on failure.**

### Alternatives considered
Mutating then rolling back on failure was rejected — rollback is harder to get right and leaves room for partial corruption.

---

## ADR-003: Bool check before int check

**Date:** 2026-10-15
**Status:** Accepted

### Context
In Python, `bool` is a subtype of `int`. So `isinstance(True, int)` returns `True`. If `affected_users` is validated with only `isinstance(value, int)`, then `True` passes and is stored as a number.

### Decision
In `validate_affected_users`, check `isinstance(value, bool)` **first**, raise if true, then check `isinstance(value, int)`.

### Consequences
- `True` and `False` are rejected with a clear error.
- `1` and `0` are still accepted as integers (but `0` is rejected by the `> 0` check).
- The saved JSON never contains a boolean in the `affected_users` field.

### Alternatives considered
Relying on the `value <= 0` check was rejected — `True <= 0` is `False`, so a boolean would sneak through.

---

## ADR-004: Atomic load — return a new list, never mutate the caller's

**Date:** 2026-10-15
**Status:** Accepted

### Context
`load_tickets(path)` reads a JSON file. If record #7 is invalid, records #1–6 must not end up in memory. The brief says: *"If any record is invalid, clearly reject the load and keep current memory unchanged."*

### Decision
`load_tickets(path)` returns a **new list**. It never mutates a list passed in by the caller. The caller assigns the result atomically:
```python
new_tickets = load_tickets(path)  # raises on failure → old tickets untouched
tickets = new_tickets             # atomic swap
Consequences
A failed load leaves the caller's memory completely unchanged.

The function is a "pure read" — it changes nothing in the caller's world.

Tests can verify this by calling load_tickets() with a corrupt file and asserting the caller's list is unchanged.

Alternatives considered
Passing the caller's list in and appending to it was rejected — a mid-load failure would leave partial data.

ADR-005: Next ID = max + 1, not len + 1
Date: 2026-10-15
Status: Accepted

Context
Ticket IDs may have gaps (e.g., T001, T003, T005). If next ID is computed as len(tickets) + 1, it will eventually collide with an existing ID.

Decision
next_ticket_id(tickets) extracts the numeric part of every ticket ID, takes the maximum, adds 1, and formats back to T + zero-padded number. Same rule for next_note_id(ticket) per ticket.

Consequences
The next ID is always higher than every existing ID.

Gaps are preserved, not filled.

No collision after reload.

Alternatives considered
len + 1 was rejected — it fails when IDs have gaps, and it recomputes the same value until a ticket is actually added, causing collisions.

ADR-006: Note IDs are per-ticket, computed from existing notes
Date: 2026-10-15
Status: Accepted

Context
Each note has an ID like N001, N002. The brief says: "A rejected note must not consume a note ID." We need an ID scheme that is safe against rejections.

Decision
Note IDs are computed from the existing notes in that ticket — take the maximum existing numeric note ID and add 1. Never use a mutable counter that increments before validation.

Consequences
A rejected note (e.g., on a resolved ticket) does not consume an ID.

Calling next_note_id() twice in a row returns the same value — it is idempotent.

Reopening a resolved ticket and adding a note continues from the last note ID.

Alternatives considered
A stored counter (ticket["next_note_id"]) was rejected — if it increments before validation, rejected notes consume IDs.

ADR-007: Validation functions are read-only
Date: 2026-10-15
Status: Accepted

Context
Validation functions are called frequently — from the CLI, from tests, from other functions. If they mutate anything, they become unsafe.

Decision
All functions in validation.py have zero side effects. They check, return a value, or raise. They never print, never mutate, never save.

Consequences
B can call any validation function as many times as needed without worrying.

Validation is a pure read operation.

The contract says: "SIDE EFFECTS: none."

Alternatives considered
Mixing validation and normalization (returning a modified copy) was considered acceptable — but the function still does not mutate the input. It returns a new value.

Summary of Invariants
These are the promises the data layer makes:

Validate-before-mutate: A function that can fail changes nothing on failure.

No partial state: The ticket collection is either fully updated or unchanged.

Atomic load: A failed JSON load leaves memory untouched.

ID continuity: Next IDs are computed from max + 1, never len + 1.

No ID consumption on rejection: Rejected notes do not consume note IDs.

Read-only validation: Validators never mutate.

Reject bool as int: True and False are rejected where integers are expected.