# Design Notes – ROSA Financial Transactions Summary Tool

This document captures high-level design decisions for Team ROSA's project.

## Initial Scope

- Load transactions from a CSV file.
- Compute basic summaries:
  - Total income
  - Total expenses
  - Net balance
- Keep the design simple and modular so that additional features can be added later,
  such as:
  - Summaries by category
  - Date range filters
  - Command-line arguments for custom reports

## Assumptions

- The dataset contains a numeric `amount` column where:
  - Positive values represent income.
  - Negative values represent expenses.
- Additional columns (e.g., `date`, `category`, `description`) may be used later.

## Next Steps

- Add validation and error handling for missing or malformed data.
- Implement optional command-line parameters to filter by date range or category.
- Expand tests in `tests/test_summary_tool.py`.
