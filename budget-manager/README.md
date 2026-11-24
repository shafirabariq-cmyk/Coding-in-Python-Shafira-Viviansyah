Personal Budget Manager (Release 1)
A command-line app to record income and expenses, list them, and report balances per currency. Data is saved to a CSV file, and every input is validated at entry.

Setup
Requires uv and Python 3.11+.

cd budget-manager
uv sync
Run
uv run budget-manager
Data is stored in data/transactions.csv (created on the first save). To start with the sample data instead:

cp data/sample_transactions.csv data/transactions.csv
uv run budget-manager
The sample file deliberately contains invalid rows. On start-up the app reports each one and loads only the valid rows:

Row 5: amount must be greater than 0.
Row 6: category must be one of: food, tuition, holiday, shopping, electricity, salary, other.
Row 7: amount must be a number, e.g. 18.50.
Row 8: date must be a real date in YYYY-MM-DD format.
Row 10: currency must be one of: EUR, USD, IDR.
Row 11: kind must be income or expense.
Loaded 5 transaction(s) from data/transactions.csv.
Example session
=== Budget Manager ===
1. Add transaction
2. List transactions
3. Report
4. Undo last transaction
5. Quit
Choose: 1
Kind (income/expense): expense
Category [food, tuition, holiday, shopping, electricity, salary, other]: gym
Error: category must be one of: food, tuition, holiday, shopping, electricity, salary, other.
Category [food, tuition, holiday, shopping, electricity, salary, other]: Food
Amount: -5
Error: amount must be greater than 0.
Amount: 12.30
Currency [EUR, USD, IDR]: eur
Date (YYYY-MM-DD, Enter = today): 2026-11-24
Saved: T012  2026-11-24  expense  food              12.30 EUR

Choose: 3
Balance per currency:
EUR  income 1500.00 | expense 930.80 | balance 569.20
IDR  income 0.00 | expense 250000.00 | balance -250000.00
USD  income 0.00 | expense 320.00 | balance -320.00

Expenses by category:
EUR  food        30.80
EUR  tuition     900.00
IDR  shopping    250000.00
USD  holiday     320.00
Test
uv run pytest -v
15 tests cover the normal case (adding a valid transaction), boundary cases (amount 0, -5, 0.01, abc; unknown category; invalid dates), reports that never mix currencies, and persistence (save/load round-trip, missing file, invalid rows skipped with row numbers, ids continuing after a reload, undo surviving a reload). Each test is labelled with the acceptance criterion it checks; see ACCEPTANCE_CRITERIA.md.

Project structure
budget-manager/
├── README.md, DESIGN.md, AI_DISCLOSURE.md, ACCEPTANCE_CRITERIA.md
├── data/sample_transactions.csv   # valid + invalid rows
├── src/budget_manager/
│   ├── models.py       # transaction schema, id generation
│   ├── validation.py   # all input rules and error messages
│   ├── services.py     # add, sort, summarize, undo (no I/O)
│   ├── storage.py      # CSV load/save
│   └── cli.py          # menu, prompts, printing
└── tests/test_budget.py

Known limitations
No filtering by category, currency or date range.
No currency conversion: balances are reported separately per currency.
No export to PDF; data is only stored as CSV.
Transactions cannot be edited; only the last one can be undone.
Invalid rows found when loading are reported and skipped. They are not kept, so the next save removes them from data/transactions.csv.
data/transactions.csv is read relative to the current folder, so the app must be run from the budget-manager/ folder.