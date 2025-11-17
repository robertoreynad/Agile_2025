# Team Charter – Financial Transactions Summary Tool

## 1. Team Members
- Kalid Sacbe Juarez Ponce
- Jose Osorio Davila
- Roberto Reyna Delgado
- Carlos Alberto Juarez Maldonado

## 2. Mission & Vision

**Mission**  
Develop a Python tool to process the *Financial Transactions Dataset* and produce clear, useful summaries of income and expenses, while applying Agile practices during a one-week sprint.

**Vision**  
Become a team that collaborates effectively using GitHub and Taiga, delivering modular, reusable code that can seamlessly integrate into a future dashboard or visualization.

## 3. Success Priorities

- Deliver a functional tool that meets all course requirements.
- Uphold high-quality Agile processes: frequent commits, branch usage with pull requests, and an up-to-date Taiga board.
- Ensure meaningful contributions from every team member.
- Provide clean, well-documented, and easily reusable code.
- Meet the deadline without last-minute workload spikes.

## 4. Working Agreements

- Primary communication channel: WhatsApp.
- Maximum response time to team messages: within 12 hours.
- Coordination meetings: two meetings during the sprint—one at the start and one at the midpoint.
- All tasks must be created and updated in Taiga before work begins.
- No direct merges to `main`: all changes require a pull request with at least one review.
- If a member cannot complete an assigned task, they must notify the team as soon as possible.

## 5. Definition of Done

A user story is considered **Done** when:

- The code is implemented and runs without errors.
- It has been reviewed by at least one teammate via pull request.
- Basic comments/docstrings are added to key functions.
- Tests or usage examples are updated as needed.
- The story is marked complete in Taiga.
- It is merged into the main branch (`main` or `master`) without conflicts.


## 6. Sprint Goal

By the end of this one-week sprint, deliver a reusable, well-documented Python package that loads, cleans, and generates key financial insights (monthly cash-flow, spending by category, top merchants, and optional charts) from the provided Financial Transactions Dataset, with full traceability in Taiga and distributed collaboration on GitHub.


## 7. User Stories and Acceptance Criteria

| ID   | As a...          | I want to...                                               | So that...                          | Points | Acceptance Criteria                                                                 |
|------|------------------|------------------------------------------------------------|-------------------------------------|--------|--------------------------------------------------------------------------------------|
| US01 | financial user   | load and clean the transactions CSV                        | I have reliable data to analyse     | 3      | • Date parsed correctly<br>• Missing values handled<br>• Duplicates removed<br>• Returns clean DataFrame |
| US02 | financial user   | see total income, expenses and net balance per month       | I can track monthly cash flow       | 3      | • Returns DataFrame with Year-Month, Income, Expense, Net                           |
| US03 | financial user   | view spending broken down by category                      | I know where my money goes          | 5      | • Returns sorted DataFrame<br>• matplotlib bar chart saved as PNG                   |
| US04 | financial user   | see my top 10 merchants by amount spent                    | I can identify biggest spending places | 3   | • Returns DataFrame<br>• Horizontal bar chart                                       |
| US05 | developer / user | run the whole analysis with one command                    | I can demo or reuse the tool easily | 3      | • `python -m financial_summary` works<br>• Prints tables<br>• Saves plots to `/output` folder |
| US06 | future developer | have clear documentation and examples                      | Anyone can understand and extend the code | 2  | • Detailed README<br>• Docstrings on all public functions<br>• `requirements.txt`   |

**Total Story Points: 19**


## 8. Project Structure

```
financial-transactions-summary/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   └── Financial_Transactions_Dataset.csv   # (add manually, gitignored if large)
├── src/
│   └── financial_summary/
│       ├── __init__.py
│       ├── loader.py
│       ├── monthly_summary.py
│       ├── category_analysis.py
│       ├── merchant_analysis.py
│       └── plots.py
├── main.py
├── tests/
│   └── test_summary_tool.py
└── output/   # (gitignored – plots go here)
```


## 9. Collaboration Workflow
- GitHub:
  - Branch-per-feature workflow (`feature/US01-loader`, etc.)
  - Pull requests with peer reviews
  - Commits tagged with user story IDs

- Taiga:
  - Backlog with user stories and story points
  - Tasks assigned and moved across columns (To Do → In Progress → Done)
  - Instructor added as project member
 
```
## 10. How to Run the Project

1. **Clone the repository:**
   git clone https://github.com/robertoreynad/Agile_2025.git
   cd Agile_2025

2. **Install dependencies:**
   Make sure you have Python 3.8 or higher installed. Then run:
   pip install -r requirements.txt

3. **Run the complete analysis:**
   python -m financial_summary

4. **Expected results:**
   - Summary tables will be printed in the terminal.
   - Charts will be saved as PNG files in the /output folder.
```

