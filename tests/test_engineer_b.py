"""test_engineer_b.py - Engineer B's tests for search, reports, and understanding check.

Aligned with the current module signatures:
- search.search_tickets(tickets_list, title_query, category, status, priority)
- search.sort_by_priority_then_id(tickets)
- search.ticket_number(ticket_id)
- understanding_check.score_answers(submitted_answers: dict)
- understanding_check.QUESTIONS (uses "correct" key)
"""

import copy
import unittest

from search import search_tickets, sort_by_priority_then_id, ticket_number
from understanding_check import score_answers, QUESTIONS


def T(i, title, cat="Network", status="open", pr="medium", notes=None):
    return {
        "id": i,
        "title": title,
        "category": cat,
        "urgency": "low",
        "affected_users": 1,
        "priority": pr,
        "status": status,
        "assigned_to": "Sam",
        "notes": notes or [],
    }


def fixture():
    return [
        T("T001", "WiFi down in Lab", "Network", "open", "high"),
        T("T002", "wi-fi slow", "Network", "resolved", "low"),
        T("T010", "Laptop battery", "Hardware", "open", "critical"),
        T("T003", "WIFI printer", "Hardware", "open", "high"),
    ]


class SearchTests(unittest.TestCase):
    def test_title_ignores_case_and_matches_substring(self):
        ids = [t["id"] for t in search_tickets(fixture(), "WI-FI")]
        self.assertEqual(ids, ["T002"])
        self.assertEqual(
            {t["id"] for t in search_tickets(fixture(), "wifi")},
            {"T001", "T003"},
        )

    def test_combined_filters_use_and(self):
        ids = [t["id"] for t in search_tickets(fixture(), "wifi", "Network", "open")]
        self.assertEqual(ids, ["T001"])

    def test_empty_filters_return_everything(self):
        self.assertEqual(len(search_tickets(fixture())), 4)

    def test_search_is_read_only(self):
        data = fixture()
        before = copy.deepcopy(data)
        results = search_tickets(data, "wifi")
        results[0]["title"] = "MUTATED"
        self.assertEqual(data, before)

    def test_invalid_filter_rejected(self):
        with self.assertRaises(ValueError):
            search_tickets(fixture(), category="Banana")

    def test_priority_sort_uses_numeric_ids(self):
        data = [
            T("T10", "a", pr="high"),
            T("T2", "b", pr="high"),
            T("T5", "c", pr="critical"),
        ]
        self.assertEqual(
            [t["id"] for t in sort_by_priority_then_id(data)],
            ["T5", "T2", "T10"],
        )
        self.assertEqual(ticket_number("T10"), 10)


class UnderstandingCheckTests(unittest.TestCase):
    def test_scoring_is_pure_and_correct(self):
        perfect = {q["id"]: q["correct"] for q in QUESTIONS}
        self.assertEqual(score_answers(perfect), 6)

        wrong = {q["id"]: "Z" for q in QUESTIONS}
        self.assertEqual(score_answers(wrong), 0)

    def test_partial_answers_score_correctly(self):
        partial = {"Q1": "B", "Q2": "C"}
        self.assertEqual(score_answers(partial), 2)

    def test_missing_answers_score_zero(self):
        self.assertEqual(score_answers({}), 0)

    def test_question_bank_has_six_questions_with_correct_key(self):
        self.assertEqual(len(QUESTIONS), 6)
        for q in QUESTIONS:
            self.assertIn("id", q)
            self.assertIn("correct", q)
            self.assertIn("options", q)
            self.assertIn(q["correct"], q["options"])


if __name__ == "__main__":
    unittest.main()