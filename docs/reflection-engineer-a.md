
# Reflection — Engineer A

**Date:** 2026-10-15
**Engineer:** [your name]

## One verified mistake

I initially believed that a function could validate *after* mutating, and that raising an error would somehow "undo" the mutation. During the conceptual quiz, I traced the code line by line and realised that when a function raises, lines below the raise never execute — but lines above the raise already changed the data. This meant a failed validation could leave a ticket corrupted.

**How I verified it:** I traced `transition_ticket(ticket, "in_progress")` on an unassigned ticket. With mutate-first, the ticket ends up `in_progress` but unassigned. With validate-first, the error raises before any change.

**The fix:** All my mutation functions now follow validate-before-mutate.

---

## One learning gain

I learned what a **side effect** is. Before this session, I thought it was just "things a function does." Now I understand it is any change to the world *besides* the return value — printing, saving, mutating a dictionary. I also learned that a function's contract must state its side effects, because Engineer B's CLI relies on those promises.

**How I verified it:** I imagined B's CLI printing "Note added." while my `add_note()` also printed "Note saved!" — the user would see two messages for one action. That confirmed: if the contract says no printing, the function must not print.

---

## One improvement received through code review

I worked solo under deadline pressure, so I did not receive a live code review this session. In a proper pairing session, I would ask my partner to review:

- Whether `validate_affected_users` correctly rejects `True` and `False`
- Whether `load_tickets` truly leaves memory unchanged on a corrupt file
- Whether the test for `next_ticket_id` covers the gap case (`T001, T003, T005` → `T006`)

I have documented these as review requests in my PR description.

---

## What I would do next

If I had more time, I would:
1. Add `validate_title` and `validate_category` to `validation.py`
2. Implement `add_note()` with the per-ticket ID rule
3. Write the atomic `load_tickets()` with full-collection validation
4. Add the two bug-hunter tests for Engineer B's module
5. Open a PR and request review from my partner

I understand the concepts now. The remaining work is execution.