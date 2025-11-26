## About the Student Incentive Platform

This platform helps tertiary institutions track and reward student participation by capturing volunteer or co-curricular hours, validating them through staff approvals, and converting approved time into accolades and leaderboard rankings. It is implemented with Flask and exposes both a command-line interface (CLI) for administrative tasks and lightweight web views for manual review and browsing.

Key capabilities:
- Student hour requests: students submit hours for confirmation.
- Staff review workflow: staff members can approve or deny requests; approvals automatically log hours.
- Accolades & leaderboards: students earn accolades and are ranked by approved hours.
- Reporting utilities: CLI commands to list users, staff, students, requests, and logged hours.

Interfaces:
- CLI: `flask` commands for initialization, user/staff/student management, and test execution.
- Web views: basic HTML templates and static assets for viewing lists, messages, and admin pages.

Intended users: administrators, staff reviewers, and students at educational institutions who need a simple system to record and validate participation hours.
## General App Commands

| Command | Description |
|---------|-------------|
| `flask init` | Creates and initializes the database |
| `flask listUsers` | Lists all users in the database |
| `flask listStaff` | Lists all staff in the database |
| `flask listStudents` | Lists all students in the database |
| `flask listAccolades` | Lists all accolades in the database |
| `flask listRequests` | Lists all requests in the database |
| `flask listApprovedRequests` | Lists all approved requests |
| `flask listPendingRequests` | Lists all pending requests |
| `flask listDeniedRequests` | Lists all denied requests |
| `flask listloggedHours` | Lists all logged hours |

---


## Student Commands

| Command | Description |
|---------|-------------|
| `flask student create` | Create a new student (interactive: enter name + email) |
| `flask student hours` | View total hours (enter student ID) |
| `flask student request` | Creates a request (--student_id, --service, --staff_id, --hours, --date) |
| `flask student requestHours` | Request hour confirmation (enter student ID + hours) |
| `flask student viewmyRequests` | List all requests made by a student (enter student ID) |
| `flask student viewmyAccolades` | List all accolades earned by a student (enter student ID) |
| `flask student viewLeaderboard` | View leaderboard of students ranked by approved hours |


---

## Staff Commands

| Command | Description |
|---------|-------------|
| `flask staff create` | Create a new staff member (interactive: enter name + email) |
| `flask staff update` | Update a staff member's attributes via options (--username, --email, and/or --password) |
| `flask staff createAccolade` | Creates a new accolade |
| `flask staff updateAccolade` | Updates an accolade's attributes |
| `flask staff deleteAccolade` | Deletes an accolade by its ID, with option to delete all history records |
| `flask staff assignAccolade` | Assigns an accolade to specific student |
| `flask staff removeAccolade` | Remove an accolade from specific student |
| `flask staff requests` | View all pending requests |
| `flask staff approveRequest` | Approve a student’s request (enter staff ID + request ID) → logs hours |
| `flask staff denyRequest` | Deny a student’s request (enter staff ID + request ID) |
| `flask staff viewLeaderboard` | View leaderboard of students ranked by approved hours |


---

## Request Commands

| Command | Description |
|---------|-------------|
| `flask request delete` | Delete a request by ID |
| `flask request update` | Update a request's attributes via options (--student_id, --service, --hours, --status) |
| `flask request search` | Command to search requests by student_id, service, or date (--student_id, --service, --date) |
---

## Accolade Commands

| Command | Description |
|---------|-------------|
| `flask accolade search` | Search accolades by accolade_id, staff_id, description, or student_id |
| `flask accolade dropAccoladeTable` | Drop accolade table (all accolade records and student-accolade associations) |

---

## Tests

Run unit and integration tests via the Flask CLI testing command. Example commands:

- `flask test user int` — or - `flask test user unit` — or `flask test user` — runs tests related to the `user` tests, including both integration (`int`) and unit (`unit`) scopes.
