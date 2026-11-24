"""Persistence: load and save transactions as CSV. No business rules here,
except calling validation at the import boundary."""
import csv
import os
from pathlib import Path

from budget_manager.models import FIELDS
from budget_manager.validation import validate_row


def load_transactions(path):
    """Read the CSV at `path`.

    Returns (transactions, errors):
    - missing file -> ([], [])  (first run, AC14)
    - invalid rows are skipped, each with a message like "Row 4: ..." (AC15)
    Row numbers match the line numbers in the file (header = row 1).
    """
    path = Path(path)
    if not path.exists():
        return [], []

    transactions, errors, seen_ids = [], [], set()
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_number, row in enumerate(reader, start=2):
            try:
                transaction = validate_row(row)
                if transaction["id"] in seen_ids:
                    raise ValueError(f"duplicate id {transaction['id']}.")
            except ValueError as e:
                errors.append(f"Row {row_number}: {e}")
                continue
            seen_ids.add(transaction["id"])
            transactions.append(transaction)
    return transactions, errors


def save_transactions(path, transactions):
    """Write all transactions to `path`, replacing its contents.

    Writes to a temporary file first, then swaps it in, so a crash halfway
    never leaves a half-written file on disk.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")
    with temp_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for t in transactions:
            writer.writerow({**t, "amount": f"{t['amount']:.2f}"})
    os.replace(temp_path, path)