"""test_bug_hunters.py - Section 06's required bug-hunter exercise.

Each engineer devises ONE previously-unlisted edge case for the OTHER
engineer's module. Documented per the brief's format in the docstring of
each test.
"""

import unittest
import tickets
import search
import notes


class TestEngineerA_HuntsEngineerBsModule(unittest.TestCase):
    """
    Bug hunt by: Engineer A, targeting search.py (Engineer B's module)

    Initial state: a ticket created with category 'Network'.

    Input: search_tickets(..., category='network') -- lowercase, as a user
    might reasonably type it.

    Expected result: search.py should reject the unnormalized category,
    because valid categories are canonical ('Network', 'Hardware',
    'Software', 'Other'). The CLI is responsible for normalizing user
    input before calling search, but the search function itself must
    reject invalid filters rather than silently returning zero matches.

    Actual result: search_tickets() raises ValueError for lowercase
    'network'. This is the intended behavior -- it forces the caller
    (cli.py) to normalize category through tickets.normalize_category()
    before calling search.

    Any code change made: added validation at the top of search_tickets()
    that raises ValueError when category/status/priority are supplied but
    not in the allowed set. This makes the contract explicit and prevents
    silent empty results from typos.
    """
    def test_search_category_filter_is_exact_match_not_case_insensitive(self):
        tickets_list = [tickets.create_ticket([], "Router issue", "Network", "high", 12)]

        # Valid canonical form matches
        self.assertEqual(len(search.search_tickets(tickets_list, category="Network")), 1)

        # Lowercase 'network' is invalid -- must raise, not silently return 0
        with self.assertRaises(ValueError):
            search.search_tickets(tickets_list, category="network")


class TestEngineerB_HuntsEngineerAsModule(unittest.TestCase):
    """
    Bug hunt by: Engineer B, targeting notes.py (Engineer A's module)

    Initial state: a ticket with no notes yet.

    Input: call notes.next_note_id(ticket) TWICE in a row without actually
    adding a note in between (e.g. the CLI previews the next ID before the
    user finishes typing their message, then the user cancels).

    Expected result: both calls return 'N001' -- previewing the next ID
    must be a read-only operation that doesn't consume anything, the same
    invariant add_note() already protects for rejected notes.

    Actual result: confirmed -- next_note_id() only reads ticket['notes'],
    it never appends or mutates, so calling it any number of times without
    an actual add_note() call is safe and idempotent.

    Any code change made: none needed; this test makes that read-only
    guarantee explicit and regression-proof.
    """
    def test_next_note_id_is_read_only_and_idempotent(self):
        ticket = tickets.create_ticket([], "Printer jam", "Hardware", "low", 1)

        first_preview = notes.next_note_id(ticket)
        second_preview = notes.next_note_id(ticket)

        self.assertEqual(first_preview, "N001")
        self.assertEqual(second_preview, "N001")
        self.assertEqual(ticket["notes"], [])  # still untouched


if __name__ == "__main__":
    unittest.main()