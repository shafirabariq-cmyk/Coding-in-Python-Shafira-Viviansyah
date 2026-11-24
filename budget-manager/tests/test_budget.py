"""Tests mapped to the acceptance criteria (AC numbers in ACCEPTANCE_CRITERIA.md)."""
import pytest

from budget_manager import services, storage
from budget_manager.validation import validate_amount, validate_category, validate_date


# Normal case
def test_add_valid_transaction_gets_first_id():  # AC1
    transactions = []
    t = services.add_transaction(transactions, "2026-09-04", "expense", "food", 18.5, "EUR")
    assert t == {"id": "T001", "date": "2026-09-04", "kind": "expense",
                 "category": "food", "amount": 18.5, "currency": "EUR"}
    assert transactions == [t]


# Boundary cases
@pytest.mark.parametrize("text", ["0", "-5"])
def test_amount_zero_or_negative_is_rejected(text):  # AC4
    with pytest.raises(ValueError, match="amount must be greater than 0."):
        validate_amount(text)


@pytest.mark.parametrize("text", ["abc", ""])
def test_amount_not_a_number_is_rejected(text):  # AC4
    with pytest.raises(ValueError, match="amount must be a number"):
        validate_amount(text)


def test_smallest_positive_amount_is_accepted():  # AC4 boundary: just above 0
    assert validate_amount("0.01") == 0.01


def test_unknown_category_rejected_but_case_is_normalised():  # AC5
    with pytest.raises(ValueError, match="category must be one of"):
        validate_category("gym")
    assert validate_category(" Food ") == "food"


@pytest.mark.parametrize("text", ["2026-13-40", "04/09/2026"])
def test_invalid_date_is_rejected(text):  # AC3
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_date(text)


def test_report_never_mixes_currencies():  # AC10
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", 1000.0, "EUR")
    services.add_transaction(transactions, "2026-09-04", "expense", "food", 18.5, "EUR")
    services.add_transaction(transactions, "2026-09-05", "expense", "shopping", 50000.0, "IDR")
    summary = services.summarize_by_currency(transactions)
    assert summary["EUR"]["balance"] == 981.5
    assert summary["IDR"] == {"income": 0.0, "expense": 50000.0, "balance": -50000.0}


# Persistence
def test_save_then_load_round_trip(tmp_path):  # AC13
    path = tmp_path / "transactions.csv"
    transactions = []
    services.add_transaction(transactions, "2026-09-04", "expense", "food", 18.5, "EUR")
    storage.save_transactions(path, transactions)
    loaded, errors = storage.load_transactions(path)
    assert loaded == transactions
    assert isinstance(loaded[0]["amount"], float)
    assert errors == []


def test_missing_file_starts_empty(tmp_path):  # AC14
    assert storage.load_transactions(tmp_path / "nope.csv") == ([], [])


def test_invalid_row_is_skipped_with_row_number(tmp_path):  # AC15
    path = tmp_path / "transactions.csv"
    path.write_text(
        "id,date,kind,category,amount,currency\n"
        "T001,2026-09-01,income,salary,1000.00,EUR\n"
        "T002,2026-09-02,expense,food,12.00,EUR\n"
        "T003,2026-09-03,expense,food,-3,EUR\n",
        encoding="utf-8",
    )
    loaded, errors = storage.load_transactions(path)
    assert [t["id"] for t in loaded] == ["T001", "T002"]
    assert errors == ["Row 4: amount must be greater than 0."]


def test_new_id_continues_after_load():  # AC16
    transactions = [{"id": "T007", "date": "2026-09-01", "kind": "income",
                     "category": "salary", "amount": 10.0, "currency": "EUR"}]
    t = services.add_transaction(transactions, "2026-09-02", "expense", "food", 1.0, "EUR")
    assert t["id"] == "T008"


def test_undo_is_persisted(tmp_path):  # Stretch: undo survives a reload
    path = tmp_path / "transactions.csv"
    transactions = []
    services.add_transaction(transactions, "2026-09-01", "income", "salary", 1000.0, "EUR")
    services.add_transaction(transactions, "2026-09-02", "expense", "food", 5.0, "EUR")
    storage.save_transactions(path, transactions)

    services.undo_last(transactions)
    storage.save_transactions(path, transactions)

    reloaded, _ = storage.load_transactions(path)
    assert [t["id"] for t in reloaded] == ["T001"]
