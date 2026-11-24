# AI Disclosure

I acknowledge the use of Claude (https://claude.ai, Anthropic) to plan and implement this practice project.

**How I used it**
- To understand the brief and translate my own requirements (category list, rejecting unknown categories, supported currencies EUR/USD/IDR, separate balances per currency, today's date as default) into testable CLI acceptance criteria (`ACCEPTANCE_CRITERIA.md`).
- To set up the project with `uv` and restructure my course repository.
- To generate the code in `src/budget_manager/`, the tests in `tests/test_budget.py`, the sample data, and first drafts of `README.md` and `DESIGN.md`.

**Prompts used include**
- "Can you guide me through this assignment?" (with the Practice 1 brief attached)
- "Could you please complete the AC for Release 1?"
- "I want to use uv init for the folder; guide me from the terminal."
- "Translate the AC into validation.py."
- "Please put everything in first, I have limited time."

**How I used the output**
I defined the business rules myself, then reviewed the generated code, ran the tests and the app on my machine, and edited the documentation. Because of limited time in this session, I used the generated implementation as a reference, and I am going through each module (validation, services, storage, CLI) so that I can explain and modify it myself.