Budget Manager: Release 1 Acceptance Criteria
Scope: a command-line (CLI) app. Release 1 = add, list, report transactions + save/load to CSV, with validation at entry points.

Transaction schema
Field	Type	Allowed values	Example
id	str	Auto-generated, unique, T + 3 digits	T001
date	str	ISO YYYY-MM-DD, must be a real date	2026-09-04
kind	str	income or expense	expense
category	str	food, tuition, holiday, shopping, electricity, salary, other	food
amount	float	Greater than 0	18.50
currency	str	EUR, USD, IDR	EUR
All six fields are always present (no optional fields).

Input cleaning policy: leading/trailing spaces are removed. kind and category are lowercased (Food becomes food), currency is uppercased (eur becomes EUR). Anything still not in the allowed list is rejected, never silently corrected.

Add transaction
AC1. Valid transaction (normal case)

Given the user chooses "Add transaction"
When they enter kind=expense, category=food, amount=18.50, currency=EUR, date=2026-09-04
Then the transaction is stored with the next id (T001 if it is the first) and appears in "List transactions".
AC2. Default date

Given the prompt Date (YYYY-MM-DD, Enter = today):
When the user presses Enter without typing
Then the date is set to today's date in ISO format (e.g. 2026-11-24).
AC3. Invalid date

When the user enters 2026-13-40 or 04/09/2026
Then the app shows Error: date must be a real date in YYYY-MM-DD format. and asks again.
AC4. Invalid amount

Input	Expected output
0	Error: amount must be greater than 0.
-5	Error: amount must be greater than 0.
abc	Error: amount must be a number, e.g. 18.50.
(empty)	Error: amount must be a number, e.g. 18.50.
After an error, the app asks again; it does not crash or return to the menu.

AC5. Category not in the list

When the user enters gym
Then the app shows Error: category must be one of: food, tuition, holiday, shopping, electricity, salary, other.
When the user enters Food, it is accepted and stored as food.
AC6. Currency not in the list

When the user enters GBP
Then the app shows Error: currency must be one of: EUR, USD, IDR.
When the user enters eur, it is accepted and stored as EUR.
AC7. Invalid kind

When the user enters transfer
Then the app shows Error: kind must be income or expense.
List transactions
AC8. List all

Given 3 saved transactions
When the user chooses "List transactions"
Then all 3 are shown, one per line, with all six fields, sorted by date.
AC9. Empty list

Given no transactions
When the user chooses "List transactions"
Then the app shows No transactions yet.
Report
AC10. Balance per currency (never mixed)

Given: income 1000 EUR, expense 18.50 EUR, expense 50000 IDR
When the user chooses "Report"
Then the app shows, per currency:
EUR  income 1000.00 | expense 18.50    | balance 981.50
IDR  income 0.00    | expense 50000.00 | balance -50000.00
Amounts in different currencies are never added together.
AC11. Expense breakdown by category

The report also shows total expense per category, separately for each currency (e.g. EUR food 18.50).
AC12. Report with no data

Given no transactions, the report shows No transactions yet. and does not crash.
Save and load
AC13. Round-trip

Given transactions were saved to data/transactions.csv
When the user quits and starts the app again
Then "List transactions" shows exactly the same transactions (same ids, values, and types; amount is a float again, not text).
AC14. Missing file

Given the data file does not exist (first run)
When the app starts
Then it starts with an empty list and no error.
AC15. Invalid rows in the file

Given a CSV where row 4 has amount -3
When the file is loaded
Then row 4 is skipped, the app shows Row 4: amount must be > 0., and all valid rows are loaded.
AC16. New ids continue after loading

Given the loaded file's highest id is T007
When the user adds a transaction
Then it gets T008 (no duplicate ids).
Out of scope for Release 1 (known limitations)
Filtering by category, currency, or date range
Export to PDF
Currency conversion between EUR/USD/IDR
Editing or deleting transactions (undo is the stretch challenge)