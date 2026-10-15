"""search.py - Read-only ticket search with combined filtering (Requirement C).

Owned by Engineer B (Milestones B1, B2). Pure function, no input()/print() --
independently testable without typing anything. cli.py's menu collects the
filter values and calls this; this never mutates the tickets list it's given.
"""

import copy
import re
from typing import Any, Dict, List, Optional

VALID_CATEGORIES = ("Network", "Hardware", "Software", "Other")
VALID_STATUSES = ("open", "in_progress", "resolved")
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
VALID_PRIORITIES = tuple(PRIORITY_ORDER)


def ticket_number(ticket_id):
    """'T10' -> 10. Numeric tie-breaker so T2 sorts before T10."""
    match = re.search(r"\d+", str(ticket_id))
    return int(match.group()) if match else float("inf")


def search_tickets(
    tickets_list: List[Dict[str, Any]],
    title_query: str = "",
    category: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return tickets matching ALL supplied filters (logical AND).

    - title_query: case-insensitive substring match against the title, using
      casefold() (more aggressive than lower(), correct for caseless text).
      Empty string means "don't filter by title".
    - category / status / priority: exact match once supplied; None or ""
      means "don't filter by that field".
    - Read-only: never modifies any ticket in tickets_list. Returns copies.
    """
    results: List[Dict[str, Any]] = []
    query = (title_query or "").strip().casefold()

    for ticket in tickets_list:
        if not isinstance(ticket, dict):
            continue
        if query and query not in str(ticket.get("title", "")).casefold():
            continue
        if category and ticket.get("category") != category:
            continue
        if status and ticket.get("status") != status:
            continue
        if priority and ticket.get("priority") != priority:
            continue
        results.append(copy.deepcopy(ticket))

    return results


def sort_by_priority_then_id(tickets):
    """Separate optional view: critical > high > medium > low, then numeric ID."""
    return sorted(
        tickets,
        key=lambda t: (PRIORITY_ORDER.get(t.get("priority"), 99), ticket_number(t.get("id"))),
    )