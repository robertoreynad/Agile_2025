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

- Primary communication channel: WhatsApp / teams group.
- Maximum response time to team messages: within 12 hours.
- Coordination meetings: Daily standup: Every day at 9:00 PM
- All tasks must be created and updated in Taiga before work begins.
- No direct merges to `main`: all changes require a pull request with at least one review.
- Progress, blockers, screenshots and PR links must be documented
- If a member cannot complete an assigned task, they must notify the team as soon as possible.

## 5. Definition of Done

A user story is considered **Done** when:

- The code is implemented and runs without errors.
- It has been reviewed by the QA rol.
- Basic comments/docstrings are added to key functions.
- Tests or usage examples are updated as needed.
- The story is marked complete in Taiga.
- It is merged into the main branch (`main`) without conflicts.


## 6. Sprint Goal

Deliver a complete Python analysis pipeline capable of:
- Loading and cleaning the transactions dataset
- Normalizing descriptions
- Categorizing income and expenses
- Generating financial summaries
- Creating visualizations
- Additionally, ensure the work is fully reflected in GitHub and Taiga following Agile practices.


## 7. User Stories and Acceptance Criteria

The project included:

Discovery User Stories (Sprint 0)
	1.	Team roles & alignment meeting
	2.	Tool scope & capabilities definition
	3.	Sprint planning ceremony
	4.	GitHub repository setup

Development User Stories (Sprint 1)
	•	US #5: Load & clean dataset
	•	US #6: Monthly income, expenses & net summary
	•	US #7: Category spending breakdown + chart
	•	US #8: Top 10 merchants by spending
	•	US #9: Full pipeline execution
	•	US #10: Documentation


## 8. Project Structure

We plan to keep the project simple and organised as a basic setup like:
To have a README and requirements, also a data folder for the dataset. It is important also, to have a src folder with modules (loader, summary, analysis, plots) and a main.py to run all.

## 9. Collaboration Workflow

aily status updates
	•	Comments, attachments, screenshots, and blockers documented per User Story

In GitHub:
  We intend to follow a branch-per-feature approach (e.g., feature/US01-loader, feature/US02-monthly-summary).
  Each change will go through a pull request, with at least one peer review before merging.
  Commits will be tagged with the corresponding User Story ID to keep a clear link between code and backlog items.

In Taiga:
  The backlog will contain all user stories, each with story points assigned.
  Within each story, we will create tasks that move across the board: New → In Progress → Ready for test → Done.
  Status updates as: Comments, attachments, screenshots, issues/bugs and blockers documented per User Story.
