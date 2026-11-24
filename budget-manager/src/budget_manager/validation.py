"""Boundary checks. Each function: raw text in -> clean value out, or ValueError
with a message the user can act on. All rules live here, in one place."""
from datetime import date

from budget_manager.models import FIELDS

# Allowed values (controlled vocabulary from the AC schema)
KINDS = ["income", "expense"]
CATEGORIES = ["food", "tuition", "holiday", "shopping", "electricity", "salary", "other"]
CURRENCIES = ["EUR", "USD", "IDR"]


def validate_kind(text):
    """AC7. ' Expense ' -> 'expense'."""
    value = text.strip().lower()
    if value not in KINDS:
        raise ValueError("kind must be income or expense.")
    return value


def validate_category(text):
    """AC5. 'Food' -> 'food'; unknown categories are rejected, never guessed."""
    value = text.strip().lower()
    if value not in CATEGORIES:
        raise ValueError(f"category must be one of: {', '.join(CATEGORIES)}.")
    return value


def validate_currency(text):
    """AC6. 'eur' -> 'EUR'."""
    value = text.strip().upper()
    if value not in CURRENCIES:
        raise ValueError(f"currency must be one of: {', '.join(CURRENCIES)}.")
    return value


def validate_amount(text):
    """AC4. '18.50' -> 18.5; '0', '-5' -> rejected; 'abc', '' -> rejected."""
    try:
        value = float(text)
    except ValueError:
        raise ValueError("amount must be a number, e.g. 18.50.")
    if value <= 0:
        raise ValueError("amount must be greater than 0.")
    return value


def validate_date(text):
    """AC2 + AC3. '' -> today's date; '2026-09-04' -> '2026-09-04';
    '2026-13-40' or '04/09/2026' -> rejected."""
    value = text.strip()
    if value == "":
        return date.today().isoformat()
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise ValueError("date must be a real date in YYYY-MM-DD format.")


def validate_row(row):
    """Validate one row read from the CSV file (import boundary, AC15).
    Returns a clean transaction dict, or raises ValueError."""
    missing = [f for f in FIELDS if not row.get(f)]
    if missing:
        raise ValueError(f"missing value for: {', '.join(missing)}.")
    tx_id = row["id"].strip()
    if not (tx_id.startswith("T") and tx_id[1:].isdigit()):
        raise ValueError("id must look like T001.")
    if row["date"].strip() == "":
        raise ValueError("date must be a real date in YYYY-MM-DD format.")
    return {
        "id": tx_id,
        "date": validate_date(row["date"]),
        "kind": validate_kind(row["kind"]),
        "category": validate_category(row["category"]),
        "amount": validate_amount(row["amount"]),
        "currency": validate_currency(row["currency"]),
    }
