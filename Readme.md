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

Our goal is to build a simple Python package that can read the dataset, clean it, and give some useful financial insights. We also want to make sure the work is clear in Taiga and that everyone collaborates through GitHub.



## 7. User Stories and Acceptance Criteria

We plan to define 7-9 user stories that guides the work. The idea is that these USs reflect the main needs of the project and connect with the technical scope we have already discussed. User stories:
- Load and clean the transaction data so it is reliable.
- Show monthly income and expenses to see cash flow.
- Break down spending by category, with a chart.
- List the top merchants where most money is spent.
- Run everything with one command to make it easy to demo.
- Add documentation and examples so future developers can understand the code.


## 8. Project Structure

We plan to keep the project simple and organised as a basic setup like:
To have a README and requirements, also a data folder for the dataset. It is important also, to have a src folder with modules (loader, summary, analysis, plots) and a main.py to run all.

## 9. Collaboration Workflow

In GitHub:
  We intend to follow a branch-per-feature approach (e.g., feature/US01-loader, feature/US02-monthly-summary).
  Each change will go through a pull request, with at least one peer review before merging.
  Commits will be tagged with the corresponding User Story ID to keep a clear link between code and backlog items.

In Taiga:
  The backlog will contain all user stories, each with story points assigned.
  Within each story, we will create tasks that move across the board: To Do → In Progress → Done.
