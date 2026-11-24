"""Command-line interface: prompts and printing only. All rules live in
validation.py, all calculations in services.py, all file work in storage.py."""
from budget_manager import services, storage
from budget_manager.validation import (
    CATEGORIES,
    CURRENCIES,
    validate_amount,
    validate_category,
    validate_currency,
    validate_date,
    validate_kind,
)

DATA_FILE = "data/transactions.csv"

MENU = """
=== Budget Manager ===
1. Add transaction
2. List transactions
3. Report
4. Undo last transaction
5. Quit"""


def ask(prompt, validator):
    """Keep asking until the validator accepts the input (no crash on bad input)."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as e:
            print(f"Error: {e}")


def format_transaction(t):
    return (f"{t['id']}  {t['date']}  {t['kind']:<7}  {t['category']:<11}  "
            f"{t['amount']:>10.2f} {t['currency']}")


def add_flow(transactions):
    kind = ask("Kind (income/expense): ", validate_kind)
    category = ask(f"Category [{', '.join(CATEGORIES)}]: ", validate_category)
    amount = ask("Amount: ", validate_amount)
    currency = ask(f"Currency [{', '.join(CURRENCIES)}]: ", validate_currency)
    tx_date = ask("Date (YYYY-MM-DD, Enter = today): ", validate_date)
    transaction = services.add_transaction(
        transactions, tx_date, kind, category, amount, currency
    )
    storage.save_transactions(DATA_FILE, transactions)
    print(f"Saved: {format_transaction(transaction)}")


def list_flow(transactions):
    if not transactions:
        print("No transactions yet.")
        return
    for t in services.sorted_by_date(transactions):
        print(format_transaction(t))


def report_flow(transactions):
    if not transactions:
        print("No transactions yet.")
        return
    print("\nBalance per currency:")
    for currency, totals in sorted(services.summarize_by_currency(transactions).items()):
        print(f"{currency}  income {totals['income']:.2f} | "
              f"expense {totals['expense']:.2f} | balance {totals['balance']:.2f}")
    breakdown = services.expenses_by_category(transactions)
    if breakdown:
        print("\nExpenses by category:")
        for (currency, category), total in sorted(breakdown.items()):
            print(f"{currency}  {category:<11} {total:.2f}")


def undo_flow(transactions):
    removed = services.undo_last(transactions)
    if removed is None:
        print("Nothing to undo.")
        return
    storage.save_transactions(DATA_FILE, transactions)
    print(f"Removed: {format_transaction(removed)}")


def run():
    transactions, errors = storage.load_transactions(DATA_FILE)
    for message in errors:
        print(message)
    print(f"Loaded {len(transactions)} transaction(s) from {DATA_FILE}.")

    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            add_flow(transactions)
        elif choice == "2":
            list_flow(transactions)
        elif choice == "3":
            report_flow(transactions)
        elif choice == "4":
            undo_flow(transactions)
        elif choice == "5":
            print("Goodbye! Your data is saved in", DATA_FILE)
            break
        else:
            print("Error: please choose 1, 2, 3, 4 or 5.")
