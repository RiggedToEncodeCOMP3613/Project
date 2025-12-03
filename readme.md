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
## CLI Commands

### App Commands

| Command | Description |
|---------|-------------|
| `flask init` | Creates and initializes the database |

### User Commands

| Command | Description |
|---------|-------------|
| `flask user list` | List all users in the database |

### Student Commands

| Command | Description |
|---------|-------------|
| `flask student create <username> <email> <password>` | Create a new student |
| `flask student search <query>` | Search for a student by name, email, or ID |
| `flask student update <student_id> [--username] [--email] [--password]` | Update a student's information |
| `flask student hours <student_id>` | View total hours for a student |
| `flask student list` | List all students in the database |
| `flask student delete <student_id>` | Delete a student by ID |
| `flask student droptable` | Delete ALL students |

### Staff Commands

| Command | Description |
|---------|-------------|
| `flask staff create <username> <email> <password>` | Create a new staff member |
| `flask staff search <query>` | Search for a staff member by name, email, or ID |
| `flask staff update <staff_id> [--username] [--email] [--password]` | Update a staff member's information |
| `flask staff list` | List all staff in the database |
| `flask staff delete <staff_id>` | Delete a staff member by ID |
| `flask staff droptable` | Delete ALL staff members |

### Request Commands

| Command | Description |
|---------|-------------|
| `flask request create <student_id> <service> <staff_id> <hours> <date>` | Create a new service hour request |
| `flask request search [--student_id] [--service] [--date]` | Search requests by student_id, service, or date |
| `flask request update <request_id> [--student_id] [--service] [--hours] [--staff_id]` | Update a request's attributes |
| `flask request approve <staff_id> <request_id>` | Staff approves a student's request |
| `flask request deny <staff_id> <request_id>` | Staff denies a student's request |
| `flask request list [--status]` | List requests in the database (optionally filter by status) |
| `flask request delete <request_id>` | Delete a service hour request by ID |
| `flask request droptable` | Delete ALL requests |

### Logged Hours Commands

| Command | Description |
|---------|-------------|
| `flask loggedhours create <student_id> <staff_id> <hours> <service> <date_completed>` | Create a logged hours entry |
| `flask loggedhours search <query>` | Search logged hours by student-id, staff-id, date or service string |
| `flask loggedhours update <log_id> [--student_id] [--staff_id] [--hours] [--status]` | Update a logged hours entry by ID |
| `flask loggedhours list` | List all logged hours in the database |
| `flask loggedhours delete <log_id>` | Delete a logged hours entry by ID |
| `flask loggedhours droptable` | Delete ALL logged hours entries |

### Accolade Commands

| Command | Description |
|---------|-------------|
| `flask accolade create <staff_id> <description>` | Create a new accolade |
| `flask accolade search [--accolade_id] [--staff_id] [--description] [--student_id]` | Search accolades by id, staff_id, description, or student_id |
| `flask accolade update <accolade_id> [--staff_id] [--description]` | Update an accolade's attributes |
| `flask accolade award <accolade_id> <student_id> <staff_id>` | Award a student to an accolade |
| `flask accolade list` | List all accolades in the database |
| `flask accolade delete <accolade_id> [--history]` | Deletes an accolade by ID |
| `flask accolade droptable` | Delete ALL accolade records |

### Milestone Commands

| Command | Description |
|---------|-------------|
| `flask milestone create <hours>` | Create a new milestone |
| `flask milestone search [--id] [--hours]` | Search for a milestone by ID or hours |
| `flask milestone update <milestone_id> <new_hours>` | Update a milestone's hours by ID |
| `flask milestone list` | List all milestones |
| `flask milestone delete <milestone_id> [--history]` | Delete a milestone by ID |
| `flask milestone droptable [--history]` | Delete all milestones |
| `flask milestone history` | List all milestone history records |

### Leaderboard Commands

| Command | Description |
|---------|-------------|
| `flask viewLeaderboard` | View leaderboard of students by approved hours |
| `flask searchLeaderboard <query>` | Search leaderboard for a specific student by name or ID |

### Activity History Commands

| Command | Description |
|---------|-------------|
| `flask history view` | View all activity history |
| `flask history view --requests` | View all request history |
| `flask history view --logged` | View all logged hours history |
| `flask history view --accolade` | View all accolade history |
| `flask history view --milestone` | View all milestone history |
| `flask history search <student_id>` | View all activity history for a student |
| `flask history search <student_id> --requests` | View request history for a student |
| `flask history search <student_id> --logged` | View logged hours history for a student |
| `flask history search <student_id> --accolade` | View accolade history for a student |
| `flask history search <student_id> --milestone` | View milestone history for a student |

### Test Commands

| Command | Description |
|---------|-------------|
| `flask test user [type]` | Run User tests (type: all/unit/int) |
