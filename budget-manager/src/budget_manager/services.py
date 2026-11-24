"""Business logic: add, list, summarize. No input(), no print(), no files here,
so every function can be tested on its own."""
from budget_manager.models import make_transaction, next_id


def add_transaction(transactions, tx_date, kind, category, amount, currency):
    """Create a transaction with the next id, append it, and return it (AC1)."""
    transaction = make_transaction(
        next_id(transactions), tx_date, kind, category, amount, currency
    )
    transactions.append(transaction)
    return transaction


def sorted_by_date(transactions):
    """All transactions, oldest first (AC8). Does not change the original list."""
    return sorted(transactions, key=lambda t: (t["date"], t["id"]))


def summarize_by_currency(transactions):
    """Income, expense and balance per currency, never mixing currencies (AC10).

    Returns e.g. {"EUR": {"income": 1000.0, "expense": 18.5, "balance": 981.5}}
    """
    summary = {}
    for t in transactions:
        totals = summary.setdefault(t["currency"], {"income": 0.0, "expense": 0.0})
        totals[t["kind"]] += t["amount"]
    for totals in summary.values():
        totals["balance"] = totals["income"] - totals["expense"]
    return summary


def expenses_by_category(transactions):
    """Total expense per (currency, category) (AC11).

    Returns e.g. {("EUR", "food"): 18.5, ("IDR", "shopping"): 50000.0}
    """
    breakdown = {}
    for t in transactions:
        if t["kind"] == "expense":
            key = (t["currency"], t["category"])
            breakdown[key] = breakdown.get(key, 0.0) + t["amount"]
    return breakdown


def undo_last(transactions):
    """Stretch challenge: remove and return the most recently added transaction
    (highest id), or None if there is nothing to undo."""
    if not transactions:
        return None
    last = max(transactions, key=lambda t: int(t["id"][1:]))
    transactions.remove(last)
    return last
