"""Transaction schema (the 'contract' every other module depends on).

A transaction is a plain dict with exactly these six fields, always present:
    {"id": "T001", "date": "2026-09-04", "kind": "expense",
     "category": "food", "amount": 18.5, "currency": "EUR"}
"""

FIELDS = ["id", "date", "kind", "category", "amount", "currency"]


def make_transaction(tx_id, tx_date, kind, category, amount, currency):
    """Build one transaction dict. Inputs are expected to be validated already."""
    return {
        "id": tx_id,
        "date": tx_date,
        "kind": kind,
        "category": category,
        "amount": amount,
        "currency": currency,
    }


def next_id(transactions):
    """Return the next id after the highest existing one: T007 -> T008 (AC16)."""
    numbers = [int(t["id"][1:]) for t in transactions]
    highest = max(numbers, default=0)
    return f"T{highest + 1:03d}"
