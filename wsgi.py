import re
import click
import pytest
import sys
from datetime import datetime
from flask.cli import with_appcontext, AppGroup
import warnings
from rich.table import Table
from rich.console import Console

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from App.main import create_app
from App.database import db, get_migrate
from App.models import Student, Staff, RequestHistory, LoggedHoursHistory
from App.controllers import get_all_users, initialize
from App.controllers.loggedHoursHistory import *
from App.controllers.student_controller import *
from App.controllers.staff_controller import *
from App.controllers.milestone import *
from App.controllers.app_controller import *
from App.controllers.activityhistory_controller import *
from App.controllers.request_controller import *
from App.controllers.accolade_controller import *
from App.controllers.date_controller import *
from App.controllers.leaderboard_controller import *



# Your Flask app code here

'''APP COMMANDS(TESTING PURPOSES)'''

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')
    
    
    
    
    
    
    
'''USER COMMANDS'''

user_cli = AppGroup('user', help='User management commands')

# List all users in the database
@user_cli.command("list", help="List all users in the database")
def list_users():
    print("\n")
    try:
        users = get_all_users()
        if not users:
            print("No users found.")
            return
        
        console = Console()
        table = Table(title="All Users")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        table.add_column("Type", style="yellow")

        for user in users:
            user_type = "Student" if hasattr(user, 'student_id') else ("Staff" if hasattr(user, 'staff_id') else "Unknown")
            user_id = user.student_id if hasattr(user, 'student_id') else (user.staff_id if hasattr(user, 'staff_id') else "N/A")
            table.add_row(
                str(user_id),
                user.username if hasattr(user, 'username') else "N/A",
                user.email if hasattr(user, 'email') else "N/A",
                user_type
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(user_cli)







'''STUDENT COMMANDS'''

student_cli = AppGroup('student', help='Student object commands')

#Command to create a new student (name, email)
@student_cli.command("create", help="Create a new student")
@click.argument("username", type=str)
@click.argument("email", type=str)
@click.argument("password", type=str)
def create_student(username, email, password):
    print("\n")
    try:
        if "@" not in email:
            raise ValueError("Invalid email address.")
        student = register_student(username, email, password)

        print(f"Created student: {student}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# Command to search students by field (name, email, or ID)
@student_cli.command("search", help="Search for a student by name, email, or ID")
@click.argument("query")
def search_student(query):
    print("\n")
    try:
        student = query_router(query)
        if not student:
            print("No student found.")
            return
        
        console = Console()
        table = Table(title="Student Search Result")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        
        table.add_row(
            str(student.student_id),
            student.username if hasattr(student, 'username') else "N/A",
            student.email if hasattr(student, 'email') else "N/A"
        )
        
        console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to update a student's information (student_id, name, email, password) via CLI options
@student_cli.command("update", help="Update a student's information")
@click.argument("student_id", type=int)
@click.option("--username", type=str, default=None, help="New username for the student")
@click.option("--email", type=str, default=None, help="New email for the student")
@click.option("--password", type=str, default=None, help="New password for the student")
def update_student_command(student_id, username, email, password):
    print("\n")
    try:
        student = Student.query.get(student_id)
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            print("\n")
            return
        
        updated_student = update_student_info(
            student_id,
            username if username else None,
            email if email else None,
            password if password else None
        )
        print(f"Updated student: {updated_student}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
#Command to view total hours for a student (student_id)
@student_cli.command("hours", help="View total hours for a student")
@click.argument("student_id", type=int)
def hours(student_id):
    print("\n")
    try:
        student = get_hours(student_id)

        name,total_hours = student
        print(f"Total hours for {name}: {total_hours}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# List all students in the database
@student_cli.command("list", help="List all students in the database")
def list_students():
    print("\n")
    try:
        students = get_all_users()
        if not students:
            print("No students found.")
            return
        
        console = Console()
        table = Table(title="All Students")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")

        for student in students:
            if hasattr(student, 'student_id'):  # Filter for student objects
                table.add_row(
                    str(student.student_id),
                    student.username if hasattr(student, 'username') else "N/A",
                    student.email if hasattr(student, 'email') else "N/A"
                )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
app.cli.add_command(student_cli) # add the group to the cli

#Command to delete a student by id (student_id)
@student_cli.command("delete", help="Delete a student by ID")
@click.argument("student_id", type=int)
def delete_student_command(student_id):
    try:
        delete_student(student_id)
        print(f"Student with ID {student_id} has been deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#Command to delete ALL students (for testing purposes)
@student_cli.command("droptable", help="Delete ALL students (testing purposes only)")
@click.confirmation_option(prompt="⚠️  Are you sure you want to delete ALL students? This action cannot be undone.")
def delete_all_students_command():
    try:
        print("Nuking all students... 💣")
        num_deleted = Student.query.delete()
        db.session.commit()
        print(f"All {num_deleted} students are gone. 💥")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
    
    
    
    
    
    
    
'''STAFF COMMANDS'''

staff_cli = AppGroup('staff', help='Staff object commands')

#Command to create a new staff member (name, email)
@staff_cli.command("create", help="Create a new staff member")
@click.argument("username", type=str)
@click.argument("email", type=str)
@click.argument("password", type=str)
def create_staff(username, email, password):
    print("\n")
    try:
        if "@" not in email:
            raise ValueError("Invalid email address.")
        staff = register_staff(username, email, password)

        print(f"Created staff member: {staff}")

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# Command to search staff by field (name, email, or ID)
@staff_cli.command("search", help="Search for a staff member by name, email, or ID")
@click.argument("query")
def search_staff(query):
    print("\n")
    try:
        staff = staff_query_router(query)
        if not staff:
            print("No staff member found.")
            return
        
        console = Console()
        table = Table(title="Staff Search Result")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")
        
        table.add_row(
            str(staff.staff_id),
            staff.username if hasattr(staff, 'username') else "N/A",
            staff.email if hasattr(staff, 'email') else "N/A"
        )
        
        console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# Command to update a staff member's information (staff_id, name, email, password) via CLI options
@staff_cli.command("update", help="Update a staff member's information")
@click.argument("staff_id", type=int)
@click.option("--username", type=str, default=None, help="New username for the staff member")
@click.option("--email", type=str, default=None, help="New email for the staff member")
@click.option("--password", type=str, default=None, help="New password for the staff member")
def update_staff_command(staff_id, username, email, password):
    print("\n")
    try:
        staff_obj = Staff.query.get(staff_id)
        if not staff_obj:
            print(f"Error: Staff with ID {staff_id} not found.")
            print("\n")
            return

        updated_staff = update_staff_info(
            staff_id,
            username if username else None,
            email if email else None,
            password if password else None
        )
        print(f"Updated staff member: {updated_staff}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# List all staff in the database
@staff_cli.command("list", help="List all staff in the database")
def list_staff():
    print("\n")
    try:
        staff_list = get_all_users()
        if not staff_list:
            print("No staff members found.")
            return
        
        console = Console()
        table = Table(title="All Staff Members")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Username", style="magenta")
        table.add_column("Email", style="green")

        for staff in staff_list:
            if hasattr(staff, 'staff_id'):  # Filter for staff objects
                table.add_row(
                    str(staff.staff_id),
                    staff.username if hasattr(staff, 'username') else "N/A",
                    staff.email if hasattr(staff, 'email') else "N/A"
                )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(staff_cli) # add the group to the cli

# Command to delete a staff member by id (staff_id)
@staff_cli.command("delete", help="Delete a staff member by ID")
@click.argument("staff_id", type=int)
def delete_staff_command(staff_id):
    try:
        delete_staff(staff_id)
        print(f"Staff member with ID {staff_id} has been deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to delete ALL staff members (for testing purposes)
@staff_cli.command("droptable", help="Delete ALL staff members (testing purposes only)")
@click.confirmation_option(prompt="⚠️  Are you sure you want to delete ALL staff members? This action cannot be undone.")
def delete_all_staff_command():
    try:
        print("Nuking all staff members... 💣")
        num_deleted = Staff.query.delete()
        db.session.commit()
        print(f"All {num_deleted} staff members are gone. 💥")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")









'''REQUEST COMMANDS'''

request_cli = AppGroup('request', help='Request object commands')

#Command to create a new request for a student (student_id, service, staff_id, hours, date_completed)
@request_cli.command("create", help="Create a new service hour request via command line options")
@click.argument("student_id", type=int)
@click.argument("service", type=str)
@click.argument("staff_id", type=int)
@click.argument("hours", type=float)
@click.argument("date", type=str)
@with_appcontext
def create_request_command_options(student_id, service, staff_id, hours, date):
    print("\n")
    try:
        request, message = create_request(student_id, service, staff_id, hours, date)
        
        if request:
            console = Console()
            table = Table(title="Request Created Successfully")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("Request ID", str(request.id))
            table.add_row("Service", request.service if hasattr(request, 'service') else "N/A")
            table.add_row("Hours", str(request.hours))
            table.add_row("Status", request.status)
            table.add_row("Message", message)
            console.print(table)
        else:
            print(f"Error: {message}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# Command to search requests by student_id, service, or date
@request_cli.command("search", help="Search requests by student_id, service, or date_completed")
@click.option("--student_id", type=int, default=None, help="Student ID to filter requests")
@click.option("--service", type=str, default=None, help="Service description to search for")
@click.option("--date", type=str, default=None, help="Date completed (YYYY-MM-DD) to filter requests")
@with_appcontext
def search_request_command(student_id, service, date):
    try:
        if student_id is None and service is None and date is None:
            print("Error: At least one search criterion (--student_id, --service, or --date) must be provided.")
            return
        
        requests, error = search_requests(student_id=student_id, service=service, date=date)
        
        if error:
            print(f"Error: {error}")
            return

        if not requests:
            print("No requests found matching the criteria.")
            return
        
        console = Console()
        table = Table(title="Search Results")
        table.add_column("Request ID", style="cyan", no_wrap=True)
        table.add_column("Student", style="magenta")
        table.add_column("Service", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Status", style="blue")
        table.add_column("Date", style="white")
        
        for req in requests:
            student = Student.query.get(req.student_id)
            student_name = student.username if student else "Unknown"
            table.add_row(
                str(req.id),
                student_name,
                req.service if hasattr(req, 'service') else "N/A",
                str(req.hours),
                req.status,
                str(req.date_completed.date()) if hasattr(req, 'date_completed') else "N/A"
            )
        
        console.print(table)
        
    except Exception as e:
        print(f"An error occurred during search: {e}")
        
@request_cli.command("update", help="Update a request's attributes (student_id, service, hours, staff_id)")
@click.argument("request_id", type=int)
@click.option("--student_id", type=int, default=None, help="New Student ID")
@click.option("--service", type=str, default=None, help="New Service description")
@click.option("--hours", type=float, default=None, help="New Hours value")
@click.option("--staff_id", type=int, default=None, help="New Staff ID")
@with_appcontext
def update_request_command(request_id, student_id, service, hours, staff_id):
    print("\n")
    if not student_id and not service and not hours and not staff_id:
        print("Error: At least one attribute (--student_id, --service, --hours, --staff_id) must be provided.")
        print("\n")
        return

    try:
        req = RequestHistory.query.get(request_id)
        if not req:
            print(f"Error: Request with ID {request_id} not found.")
            print("\n")
            return
        
        request, message = update_request_entry(request_id, student_id, service, hours, staff_id=staff_id)

        if request:
            print(f"Successfully updated Request ID {request.id}: {message}")
        else:
            print(f"Error: {message}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
#Command for staff to approve a student's request (staff_id, request_id)
#Once approved it is added to logged hours database
@request_cli.command("approveRequest", help="Staff approves a student's request")
@click.argument("staff_id", type=int)
@click.argument("request_id", type=int)
def approveRequest(staff_id, request_id):
    print("\n")
    try:
        results = process_request_approval(staff_id, request_id)
    
        req=results['request']
        student_name=results['student_name']
        staff_name=results['staff_name']
        logged=results['logged_hours']

        if logged:
            print(f"Request {request_id} for {req.hours} hours made by {student_name} approved by Staff {staff_name} (ID: {staff_id}). Logged Hours ID: {logged.id}")
        else:
            print(f"Request {request_id} for {req.hours} hours made by {student_name} could not be approved (Already Processed).")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# Command for staff to deny a student's request (staff_id, request_id)
#change request status to denied, no logged hours created
@request_cli.command("denyRequest", help="Staff denies a student's request") 
@click.argument("staff_id", type=int)
@click.argument("request_id", type=int)
def denyRequest(staff_id, request_id):
    print("\n")
    try:
        results = process_request_denial(staff_id, request_id)

        req=results['request']
        student_name=results['student_name']
        staff_name=results['staff_name']
        success=results['denial_successful']

        if success:
            print(f"Request {request_id} for {req.hours} hours made by {student_name} denied by Staff {staff_name} (ID: {staff_id}).")
        else:
            print(f"Request {request_id} for {req.hours} hours made by {student_name} could not be denied (Already Processed).")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# List requests in the database with optional status filter
@request_cli.command("list", help="List requests in the database (optionally filter by status)")
@click.option("--status", type=click.Choice(["all", "approved", "pending", "denied"], case_sensitive=False), default="all", help="Filter by request status (default: all)")
def list_requests(status):
    print("\n")
    try:
        if status.lower() == "all":
            requests = RequestHistory.query.all()
            title = "All Requests"
        else:
            requests = RequestHistory.query.filter_by(status=status.lower()).all()
            title = f"{status.capitalize()} Requests"
        
        if not requests:
            print(f"No {title.lower()} found.")
            return
        
        console = Console()
        table = Table(title=title)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Student ID", style="magenta")
        table.add_column("Service", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Status", style="blue")
        table.add_column("Date", style="white")

        for request in requests:
            table.add_row(
                str(request.id),
                str(request.student_id),
                request.service if hasattr(request, 'service') else "N/A",
                str(request.hours),
                request.status,
                str(request.date_completed.date()) if hasattr(request, 'date_completed') else "N/A"
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
        
app.cli.add_command(request_cli) 

# Command to delete a request by ID
@request_cli.command("delete", help="Delete a service hour request by ID")
@click.argument("request_id", type=int)
def delete_request(request_id):
    print("\n")
    try:
        success, message = delete_request_entry(request_id)
        
        if success:
            print(f"Success: {message}")
        else:
            print(f"Error: {message}")
    
    except ValueError:
        print("Error: Request ID must be an integer.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to drop request table (all request records and associated activity records)
@request_cli.command("droptable", help="Drops all request records from the database (WARNING: IRREVERSIBLE)")
@click.confirmation_option(prompt="Are you sure you want to delete ALL request records? This cannot be undone")
@with_appcontext
def drop_request_table_command():
    print("\n")
    try:
        result, error = drop_request_table()
        
        if error:
            print(f"Error: {error}")
            print("\n")
            return
        
        print(f"Request table dropped successfully!")
        print(f"Requests deleted: {result['requests_deleted']}")
        print(f"Associated activity records cleaned up")
        print(f"\nAll request records have been permanently removed from the database.")
        
    except Exception as e:
        print(f"An error occurred during drop operation: {e}")
    print("\n")
    
    
    
    
    
    
    
'''LOGGED HOURS COMMANDS'''

logged_hours_cli = AppGroup('loggedhours', help='Logged hours commands')

# Command to create a logged hours entry
@logged_hours_cli.command("create", help="Create a logged hours entry")
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("hours", type=float)
@click.argument("service", type=str)
@click.argument("date_completed", type=str)
def create_logged_hours_command(student_id, staff_id, hours, service, date_completed):
    print("\n")
    try:
        # create_logged_hours now requires (student_id, staff_id, hours, service, date_completed)
        log = create_logged_hours(student_id, staff_id, hours, service, date_completed)
        print(f"Created logged hours entry: {log}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# Command to search logged hours by student-id, staff-id, or date
@logged_hours_cli.command("search", help="Search logged hours by student-id, staff-id, date or service string. Dates follow YYYY-MM-DD format. Date ranges use YYYY-MM-DD:YYYY-MM-DD format.")
@click.argument("query")
def search_logged_hours_command(query):
    search_type = detect_query_type(query)
    try:
        results = search_logged_hours(query, search_type)
        if not results:
            print(f"No logged hours entries found for {search_type} '{query}'.")
            return
        
        console = Console()
        table = Table(title=f"Search Results - {search_type}: {query}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Student ID", style="magenta")
        table.add_column("Staff ID", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Status", style="blue")
        table.add_column("Service", style="white")
        table.add_column("Timestamp", style="bold")

        for log in results:
            table.add_row(
                str(log.id),
                str(log.student_id),
                str(log.staff_id),
                str(log.hours),
                log.status,
                log.service if hasattr(log, 'service') and log.service else "N/A",
                str(log.timestamp) if hasattr(log, 'timestamp') else "N/A"
            )
        
        console.print(table)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
# Command to update a logged hours entry by ID
@logged_hours_cli.command("update", help="Update a logged hours entry by ID")
@click.argument("log_id", type=int)
@click.option("--student_id", type=int, default=None, help="New student ID")
@click.option("--staff_id", type=int, default=None, help="New staff ID")
@click.option("--hours", type=float, default=None, help="New hours")
@click.option("--status", type=str, default=None, help="New status")
def update_logged_hours_command(log_id, student_id, staff_id, hours, status):
    print("\n")
    try:
        log = LoggedHoursHistory.query.get(int(log_id))
        if not log:
            print(f"Error: LoggedHoursHistory entry with id {log_id} not found.")
            print("\n")
            return
        if student_id is not None:
            log.student_id = student_id
        if staff_id is not None:
            log.staff_id = staff_id
        if hours is not None:
            log.hours = hours
        if status is not None:
            log.status = status
        db.session.commit()
        print(f"Updated logged hours entry: {log}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(logged_hours_cli)

# List all logged hours in the database
@logged_hours_cli.command("list", help="List all logged hours in the database")
def list_logged_hours():
    print("\n")
    try:
        logged_hours = LoggedHoursHistory.query.all()
        if not logged_hours:
            print("No logged hours found.")
            return
        
        console = Console()
        table = Table(title="All Logged Hours")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Student ID", style="magenta")
        table.add_column("Staff ID", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Service", style="white")
        table.add_column("Timestamp", style="bold")

        for log in logged_hours:
            table.add_row(
                str(log.id),
                str(log.student_id),
                str(log.staff_id),
                str(log.hours),
                log.service if hasattr(log, 'service') and log.service else "N/A",
                str(log.timestamp) if hasattr(log, 'timestamp') else "N/A"
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# Command to delete a logged hours entry by ID
@logged_hours_cli.command("delete", help="Delete a logged hours entry by ID")
@click.argument("log_id", type=int)
def delete_logged_hours_command(log_id):
    try:
        delete_logged_hours(log_id)
        print(f"Logged hours entry with ID {log_id} has been deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to delete ALL logged hours entries (for testing purposes)
@logged_hours_cli.command("droptable", help="Delete ALL logged hours entries (testing purposes only)")
@click.confirmation_option(prompt="⚠️ Are you sure you want to delete ALL logged hours entries? This action cannot be undone.")
def delete_all_logged_hours_command():
    try:
        print ("Nuking all logged hours entries... 💣")
        num_deleted = delete_all_logged_hours()
        print(f"All {num_deleted} logged hours entries have been deleted. 💥")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
        
        
        
        

'''ACCOLADE COMMANDS'''

accolade_cli = AppGroup('accolade', help='Accolade search commands')

#Command to create a new accolade (staff_id, description) 
@accolade_cli.command("create", help="Create a new accolade")
@click.argument("staff_id", type=int)
@click.argument("description", type=str)
@with_appcontext
def create_accolade_command(staff_id, description):
    print("\n")
    try:
        staff_obj = Staff.query.get(staff_id)
        if not staff_obj:
            print(f"Error: Staff with ID {staff_id} not found.")
            print("\n")
            return
        
        accolade, error = create_accolade(staff_id, description)
        
        if error:
            print(f"Error: {error}")
        else:
            console = Console()
            table = Table(title="Accolade Created Successfully")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("ID", str(accolade.id))
            table.add_row("Description", description)
            table.add_row("Created by Staff ID", str(staff_id))
            console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to search accolades by id, staff_id, description, or student_id
@accolade_cli.command("search", help="Search accolades by id, staff_id, description, or student_id")
@click.option("--accolade_id", type=int, default=None, help="Accolade ID to search for")
@click.option("--staff_id", type=int, default=None, help="Staff ID who created the accolade")
@click.option("--description", type=str, default=None, help="Text to match in accolade description")
@click.option("--student_id", type=int, default=None, help="Student ID to filter accolades for")
@with_appcontext
def search_accolade_command(accolade_id, staff_id, description, student_id):
    try:
        accolades, error = search_accolades(
            accolade_id=accolade_id,
            staff_id=staff_id,
            description=description,
            student_id=student_id
        )
        if error:
            print(f"Error: {error}")
            return

        if not accolades:
            print("No accolades found matching the criteria.")
            return

        console = Console()
        table = Table(title="Accolade Search Results")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        table.add_column("Staff ID", style="green")
        table.add_column("Students Assigned", style="yellow")
        
        for accolade in accolades:
            num_students = len(accolade.students) if hasattr(accolade, 'students') else 0
            table.add_row(
                str(accolade.id),
                accolade.description,
                str(accolade.staff_id),
                str(num_students)
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred during search: {e}")
        
#Command to update an accolade's attributes (staff_id, description)
@accolade_cli.command("update", help="Update an accolade's attributes")
@click.argument("accolade_id", type=int)
@click.option("--staff_id", type=int, default=None, help="New staff ID")
@click.option("--description", type=str, default=None, help="New description")
@with_appcontext
def update_accolade_command(accolade_id, staff_id, description):
    print("\n")
    if staff_id is None and description is None:
        print("Error: At least one attribute (--staff_id or --description) must be provided.")
        print("\n")
        return

    try:
        from App.models.accolade import Accolade
        accolade_obj = Accolade.query.get(accolade_id)
        if not accolade_obj:
            print(f"Error: Accolade with ID {accolade_id} not found.")
            print("\n")
            return
        
        result, error = update_accolade(accolade_id, staff_id=staff_id, description=description)

        if error:
            print(f"Error: {error}")
        else:
            accolade = result.get('accolade')
            console = Console()
            table = Table(title="Accolade Updated Successfully")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("ID", str(accolade.id))
            table.add_row("Description", accolade.description)
            if result.get('updated_fields'):
                table.add_row("Updated Fields", ", ".join(result.get('updated_fields', [])))
            console.print(table)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
#Command to award a student to an accolade (accolade_id, student_id, staff_id)    
@accolade_cli.command("award", help="Award a student to an accolade")
@click.argument("accolade_id", type=int)
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
def assign_accolade_command(accolade_id, student_id, staff_id):
    print("\n")
    try:
        from App.models.accolade import Accolade
        accolade_obj = Accolade.query.get(accolade_id)
        student_obj = Student.query.get(student_id)
        staff_obj = Staff.query.get(staff_id)
        
        if not accolade_obj:
            print(f"Error: Accolade with ID {accolade_id} not found.")
            print("\n")
            return
        if not student_obj:
            print(f"Error: Student with ID {student_id} not found.")
            print("\n")
            return
        if not staff_obj:
            print(f"Error: Staff with ID {staff_id} not found.")
            print("\n")
            return
        
        result, error = assign_accolade_to_student(accolade_id, student_id, staff_id)
        
        if error:
            print(f"Error: {error}")
        else:
            accolade = result['accolade']
            student = result['student']
            history = result['history']
            
            console = Console()
            table = Table(title="Student Assigned to Accolade Successfully")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("Accolade ID", str(accolade.id))
            table.add_row("Description", accolade.description)
            table.add_row("Student ID", str(student.student_id))
            table.add_row("Assigned by Staff ID", str(staff_id))
            table.add_row("History Record ID", str(history.id))
            table.add_row("Timestamp", str(history.timestamp))
            console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
# List all accolades in the database
@accolade_cli.command("list", help="List all accolades in the database")
def list_accolades():
    print("\n")
    try:
        from App.models.accolade import Accolade
        accolades = Accolade.query.all()
        if not accolades:
            print("No accolades found.")
            return
        
        console = Console()
        table = Table(title="All Accolades")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        table.add_column("Created by Staff ID", style="green")
        table.add_column("Students Assigned", style="yellow")

        for accolade in accolades:
            num_students = len(accolade.students) if hasattr(accolade, 'students') else 0
            table.add_row(
                str(accolade.id),
                accolade.description,
                str(accolade.staff_id),
                str(num_students)
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(accolade_cli)

#Command to delete an accolade by its ID, with option to delete all history records
@accolade_cli.command("delete", help="Deletes an accolade by ID")
@click.argument("accolade_id", type=int)
@click.option("--history", is_flag=True, help="Also delete all history records for this accolade")
def delete_accolade_command(accolade_id, history):
    print("\n")
    try:
        from App.models.accolade import Accolade
        accolade_obj = Accolade.query.get(accolade_id)
        if not accolade_obj:
            print(f"Error: Accolade with ID {accolade_id} not found.")
            print("\n")
            return
        
        success, result = delete_accolade(accolade_id, delete_history=history)
        
        if not success:
            print(f"Error: {result}")
        else:
            console = Console()
            table = Table(title="Accolade Deleted Successfully")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("ID", str(accolade_id))
            table.add_row("Description", result['description'])
            if history:
                table.add_row("History Records Deleted", str(result['history_deleted']))
                if result['empty_activities_deleted'] > 0:
                    table.add_row("Activities Cleaned Up", str(result['empty_activities_deleted']))
            else:
                table.add_row("History Records", "Preserved")
            console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to drop accolade table (all accolade records and student-accolade associations)
@accolade_cli.command("droptable", help="Drops all accolade records from the database (WARNING: IRREVERSIBLE)")
@click.confirmation_option(prompt="Are you sure you want to delete ALL accolade records? This cannot be undone")
@with_appcontext
def drop_accolade_table_command():
    print("\n")
    try:
        result, error = drop_accolade_table()
        
        if error:
            print(f"Error: {error}")
            print("\n")
            return
        
        print(f"Accolade table dropped successfully!")
        print(f"Accolades deleted: {result['accolades_deleted']}")
        print(f"Student-accolade associations cleared")
        print(f"History records preserved")
        print(f"\nAll accolade records have been permanently removed from the database.")
        
    except Exception as e:
        print(f"An error occurred during drop operation: {e}")
    print("\n")
    
    
    
    
    
    
    
'''MILESTONE COMMANDS'''

milestone_cli = AppGroup('milestone', help='Milestone commands')

@milestone_cli.command("create", help="Create a new milestone")
@click.argument("hours", type=int)
def create_milestone_command(hours):
    print("\n")
    try:
        milestone = create_milestone(hours)
        print(f"Created milestone: {milestone}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
@milestone_cli.command("search", help="Search for a milestone by ID or hours")
@click.option("--id", "milestone_id", type=int, default=None, help="The ID of the milestone to search for.")
@click.option("--hours", "hours", type=int, default=None, help="The hour value of the milestone to search for.")
def search_milestone_command(milestone_id, hours):
    print("\n")
    try:
        if not milestone_id and not hours:
            print("Please provide either --id or --hours to search.")
            return

        milestones = search_milestones(milestone_id=milestone_id, hours=hours)

        if not milestones:
            print("No milestones found matching your criteria.")
            return
        
        console = Console()
        table = Table(title="Search Results")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Hours", style="magenta")

        for milestone in milestones:
            table.add_row(str(milestone['id']), str(milestone['hours']))
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


@milestone_cli.command("update", help="Update a milestone's hours by ID")
@click.argument("milestone_id", type=int)
@click.argument("new_hours", type=int)
def update_milestone_command(milestone_id, new_hours):
    print("\n")
    try:
        milestone = update_milestone(milestone_id, new_hours)
        if milestone:
            print(f"Milestone ID {milestone_id} updated to {new_hours} hours.")
        else:
            print(f"Milestone with ID {milestone_id} not found.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

@milestone_cli.command("list", help="List all milestones")
def list_milestones_command():
    print("\n")
    try:
        milestones = list_all_milestones()
        if not milestones:
            print("No milestones found.")
            return
        
        console = Console()
        table = Table(title="Milestones")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Hours", style="magenta")

        for milestone in milestones:
            table.add_row(str(milestone['id']), str(milestone['hours']))
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

@milestone_cli.command("delete", help="Delete a milestone by ID")
@click.argument("milestone_id", type=int)
@click.option("--history", is_flag=True, help="Also delete associated milestone history records.")
def delete_milestone_command(milestone_id, history):
    print("\n")
    try:
        if delete_milestone(milestone_id, delete_history=history):
            print(f"Milestone with ID {milestone_id} deleted successfully.")
        else:
            print(f"Milestone with ID {milestone_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


@milestone_cli.command("droptable", help="Delete all milestones")
@click.option("--history", is_flag=True, help="Also delete associated milestone history records.")
def drop_milestones_table_command(history):
    print("\n")
    try:
        num_deleted = delete_all_milestones(delete_history=history)
        print(f"Deleted {num_deleted} milestones.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

@milestone_cli.command("history", help="List all milestone history records")
def list_milestone_history_command():
    print("\n")
    try:
        history_records = list_all_milestone_history()
        if not history_records:
            print("No milestone history records found.")
            return
        
        console = Console()
        table = Table(title="Milestone History")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Milestone ID", style="magenta")
        table.add_column("Student ID", style="green")
        table.add_column("Hours", style="yellow")
        table.add_column("Timestamp", style="blue")

        for record in history_records:
            table.add_row(
                str(record['id']),
                str(record['milestone_id']),
                str(record['student_id']),
                str(record['hours']),
                record['timestamp']
            )
        
        console.print(table)

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


app.cli.add_command(milestone_cli) # add the group to the cli







'''LEADERBOARD COMMANDS'''
@app.cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    print("\n")
    try:
        leaderboard = generate_leaderboard()

        if not leaderboard:
            print("No students found or hour data found.")
            return
        
        console = Console()
        table = Table(title="Leaderboard (by Approved Hours)")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Student Name", style="magenta")
        table.add_column("Student ID", style="green")
        table.add_column("Hours", style="yellow")

        for rank, data in enumerate(leaderboard, 1):
            table.add_row(
                str(rank),
                data['name'],
                str(data['student_id']),
                str(data['hours'])
            )
        
        console.print(table)
            
    except Exception as e:
        print(f"An error occurred while generating the leaderboard: {e}")
        
@app.cli.command("searchLeaderboard", help="Search leaderboard for a specific student by name or ID")
@click.argument("query")
def searchLeaderboard(query):
    print("\n")
    try:
        leaderboard = generate_leaderboard()

        if not leaderboard:
            print("No students found or hour data found.")
            return
        
        results = []
        for rank, data in enumerate(leaderboard, 1):
            if query.lower() in data['name'].lower() or query == str(data['student_id']):
                results.append((rank, data))
        
        if not results:
            print(f"No matching student found in the leaderboard for '{query}'.")
            return
        
        console = Console()
        table = Table(title=f"Leaderboard Search Results - '{query}'")
        table.add_column("Rank", style="cyan", no_wrap=True)
        table.add_column("Student Name", style="magenta")
        table.add_column("Student ID", style="green")
        table.add_column("Hours", style="yellow")

        for rank, data in results:
            table.add_row(
                str(rank),
                data['name'],
                str(data['student_id']),
                str(data['hours'])
            )
        
        console.print(table)
        
    except Exception as e:
        print(f"An error occurred while searching the leaderboard: {e}")




'''ACTIVITY HISTORY COMMANDS'''

history_cli = AppGroup('history', help='Activity history search commands')

# Command to list activity history (all or by type)
@history_cli.command("view", help="View activity history (all / request / logged / accolade / milestone)")
@click.argument("student_id", type=int)
@click.option("--type", type=click.Choice(["all", "request", "logged", "accolade", "milestone"], case_sensitive=False), default="all", help="Type of history to view")
def viewHistory(student_id, type):
    print("\n")
    try:
        type_choice = type.lower()

        if type_choice in ("all", "a"):
            history = list_all_acivity_history(student_id)
        elif type_choice in ("request", "requests", "r"):
            history = list_all_student_requests_history(student_id)
        elif type_choice in ("logged", "loggedhours", "l"):
            history = list_all_student_logged_hours_history(student_id)
        elif type_choice in ("accolade", "accolades", "c"):
            history = list_all_student_accolades_history(student_id)
        elif type_choice in ("milestone", "milestones", "m"):
            history = list_all_student_milestones_history(student_id)
        else:
            print(f"Unknown type '{type_choice}'. Use one of: all, request, logged, accolade, milestone.")
            return

        if not history:
            print(f"No activity history found for student {student_id} (type: {type_choice}).")
            return

        console = Console()
        table = Table(title=f"Activity History for Student {student_id} (type: {type_choice})")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Details", style="magenta")
        
        for entry in history:
            table.add_row(str(entry.id) if hasattr(entry, 'id') else "N/A", str(entry))
        
        console.print(table)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


# Command to search activity history by type and id
@history_cli.command("search", help="Search activity history by type and id")
@click.argument("type", type=click.Choice(["activity", "student", "all", "request", "logged", "accolade", "milestone"], case_sensitive=False))
@click.option("--activity_id", type=int, default=None, help="Activity history ID (for type=activity)")
@click.option("--student_id", type=int, default=None, help="Student ID (for types: student, all, request, logged, accolade, milestone)")
@click.option("--request_id", type=int, default=None, help="Request ID (for type=request)")
@click.option("--loggedhours_id", type=int, default=None, help="Logged hours ID (for type=logged)")
@click.option("--accolade_id", type=int, default=None, help="Accolade history ID (for type=accolade)")
@click.option("--milestone_id", type=int, default=None, help="Milestone history ID (for type=milestone)")
def searchHistory(type, activity_id, student_id, request_id, logged_hours_id, accolade_id, milestone_id):
    print("\n")
    try:
        type_choice = type.lower()

        # Search by activity id does not need a student id
        if type_choice in ("activity", "act"):
            if not activity_id:
                print("Error: --activity-id is required for type=activity")
                return
            result = search_history_by_activity(activity_id)
            if not result:
                print(f"No activity history found for activity id {activity_id}.")
                return
            for entry in result:
                print(entry)
            return

        # For types that require a student id, check it's provided now
        if not student_id:
            print(f"Error: --student-id is required for type={type_choice}")
            return

        if type_choice in ("all",):
            result = search_history_by_student(student_id)
            if not result:
                print(f"No activity history found for student {student_id}.")
                return
            for entry in result:
                print(entry)
            return

        if type_choice in ("request", "requests"):
            if not request_id:
                print("Error: --request-id is required for type=request")
                return
            result = search_history_by_request(student_id, request_id)
        elif type_choice in ("logged", "loggedhours"):
            if not logged_hours_id:
                print("Error: --logged-hours-id is required for type=logged")
                return
            result = search_history_by_logged_hours(student_id, logged_hours_id)
        elif type_choice in ("accolade", "accolades"):
            if not accolade_id:
                print("Error: --accolade-id is required for type=accolade")
                return
            result = search_history_by_accolade(student_id, accolade_id)
        elif type_choice in ("milestone", "milestones"):
            if not milestone_id:
                print("Error: --milestone-id is required for type=milestone")
                return
            result = search_history_by_milestone(student_id, milestone_id)
        else:
            print(f"Unknown type '{type_choice}'. Use one of: activity, student/all, request, logged, accolade, milestone.")
            return

        if not result:
            print("No matching entry found.")
            return

        print("Search result:")
        print(result)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(history_cli)


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests or StudentUnitTests or StaffUnitTests or RequestUnitTests or LoggedHoursUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests or StudentIntegrationTests or StaffIntegrationTests "]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)