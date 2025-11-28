import re
import click, pytest, sys
from datetime import datetime
from flask.cli import with_appcontext, AppGroup

from App.controllers.loggedHoursHistory import search_logged_hours
from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.models import RequestHistory
from App.models import LoggedHoursHistory
from App.main import create_app
from App.controllers.student_controller import delete_student, query_router, register_student, get_approved_hours, create_hours_request, fetch_requests, fetch_accolades, generate_leaderboard, update_student_info
from App.controllers.staff_controller import *
from App.controllers.app_controller import *
from App.controllers.activityhistory_controller import *
from App.controllers.request_controller import *
from App.controllers.accolade_controller import *
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


'''APP COMMANDS(TESTING PURPOSES)'''

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')


@app.cli.command("listUsers", help="Lists all users in the database")
def listUsers():
    listAllUsers()


#Comamand to list all staff in the database
@app.cli.command ("listStaff", help="Lists all staff in the database")
def listStaff():
    printAllStaff()


#Comamand to list all students in the database
@app.cli.command ("listStudents", help="Lists all students in the database")
def listStudents():
    printAllStudents()
    
#Command to search students by field


#Comamand to list all accolades in the database
@app.cli.command ("listAccolades", help="Lists all accolades in the database")
def listAccolades():
    listAllAccolades()

#Comamand to list all requests in the database
@app.cli.command ("listRequests", help="Lists all requests in the database")
def listRequests():
    listAllRequests()


#Comamand to list all approved requests in the database
@app.cli.command ("listApprovedRequests", help="Lists all approved requests in the database")
def listApprovedRequests():
    listAllApprovedRequests()


#Comamand to list all pending requests in the database
@app.cli.command ("listPendingRequests", help="Lists all pending requests in the database")
def listPendingRequests():
    listAllPendingRequests()


#Comamand to list all denied requests in the database
@app.cli.command ("listDeniedRequests", help="Lists all denied requests in the database")
def listDeniedRequests():
    listAllDeniedRequests()


#Comamand to list all logged hours in the database
@app.cli.command ("listloggedHours", help="Lists all logged hours in the database")
def listloggedHours():
    listAllloggedHours()



'''STUDENT COMMANDS'''

student_cli = AppGroup('student', help='Student object commands')

# Command to search students by field (name, email, or ID)
@student_cli.command("search", help="Search for a student by name, email, or ID")
@click.argument("query")
def search_student(query):
    print("\n")
    try:
        student = query_router(query)
        print(f"Found student: {student}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to view total approved hours for a student (student_id)
@student_cli.command("hours", help="View total approved hours for a student")

def hours ():
    print("\n")
    try:
        student_id = int(input("Enter your student ID: "))

        student = get_approved_hours(student_id)

        name,total_hours = student
        print(f"Total approved hours for {name}: {total_hours}")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to create a new student (name, email)
@student_cli.command("create", help="Create a new student")
def create_student():
    print("\n")
    try:
        name = input("Enter student name: ")
        email = input("Enter student email: ")
        if "@" not in email:
            raise ValueError("Invalid email address.")
        password = input("Enter student password: ")    
        student = register_student(name, email, password)

        print(f"Created student: {student}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to delete a student by id (student_id)
@student_cli.command("delete", help="Delete a student by ID")
def delete_student_command():
    student_id = int(input("Enter the student ID to delete: "))
    try:
        delete_student(student_id)
        print(f"Student with ID {student_id} has been deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
#Command to delete ALL students (for testing purposes)
@student_cli.command("deleteAll", help="Delete ALL students (testing purposes only)")
def delete_all_students_command():
    confirmation = input("\033[91m\033[5m⚠️  Are you sure you want to delete ALL students? This action cannot be undone. (yes/no): ⚠️\033[0m ")
    if confirmation.lower() == 'yes':
        try:
            print("Nuking all students... 💣")
            num_deleted = Student.query.delete()
            db.session.commit()
            print(f"All {num_deleted} students are gone. 💥")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
    else:
        print("Operation cancelled.")

#Command to update a student's information (student_id, name, email, password) via CLI options
@student_cli.command("update", help="Update a student's information")
@click.argument("student_id", type=int)
@click.option("--name", default=None, help="New name for the student")
@click.option("--email", default=None, help="New email for the student")
@click.option("--password", default=None, help="New password for the student")
def update_student_command(student_id, name, email, password):
    print("\n")
    try:
        updated_student = update_student_info(
            student_id,
            name if name else None,
            email if email else None,
            password if password else None
        )
        print(f"Updated student: {updated_student}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

#Command to create a new request for a student (student_id, service, staff_id, hours, date_completed)
@student_cli.command("request", help="Create a new service hour request via command line options")
@click.option("--student_id", required=True, type=int, help="ID of the student making the request")
@click.option("--service", required=True, help="Description of the service performed")
@click.option("--staff_id", required=True, type=int, help="ID of the staff member to verify")
@click.option("--hours", required=True, type=float, help="Number of hours to claim")
@click.option("--date", required=True, help="Date of service (YYYY-MM-DD)")
@with_appcontext
def create_request_command_options(student_id, service, staff_id, hours, date):
    """
    Creates a new request for a student using command line options.
    Usage: flask student request --student_id 1 --service "Gardening" --staff_id 2 --hours 4 --date 2023-10-25
    """
    request, message = create_request(student_id, service, staff_id, hours, date)
    
    if request:
        click.echo(f"\nSuccess: {message}")
        click.echo(f"Request ID: {request.id}")
        click.echo(f"Status: {request.status}")
        click.echo(f"Details: {request}") 
    else:
        click.echo(f"\nError: {message}")

#Command for student to request hour confirmation (student_id, hours)
@student_cli.command("requestHours", help="Student requests hour confirmation (interactive)")
def requestHours():
    print("\n")
    try:
        student_id = int(input("Enter your student ID: "))
        hours = float(input("Enter the number of hours to request: "))
    
        req = create_hours_request(student_id,hours)
        print(f"Requested {hours} hours for confirmation.\n")
        print(f"Request ID: {req.id}, Status: {req.status}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print("\n")


#command to list all requests made by a specific student(student_id)
@student_cli.command("viewmyRequests", help="List all requests for a student")
def viewmyRequests():
    print("\n")
    try:
        student_id = int(input("Enter your student ID: "))
        requests = fetch_requests(student_id)

        if not requests:
            print(f"No requests found for student {student_id}.")
            return
        else:
            print(f"Requests for student {student_id}:")
            for req in requests:
                print(req)
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


#command to list all accolades for a specific student (student_id)
@student_cli.command("viewmyAccolades", help="List all accolades for a student")
def viewmyAccolades():
    print("\n")
    try:
        student_id = int(input("Enter your student ID: "))
        accolades = fetch_accolades(student_id)

        if not accolades:
            print(f"No accolades found for student {student_id}.")
            return
        else:
            print(f"Accolades for student {student_id}:")
            for accolade in accolades:
                print(f"- {accolade}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
app.cli.add_command(student_cli) # add the group to the cli


# Student command to list activity history (all or by type)
@student_cli.command("viewHistory", help="View activity history (all / request / logged / accolade / milestone)")
def viewHistory():
    print("\n")
    try:
        student_id = int(input("Enter your student ID: "))
        print("Select type to view: [all/request/logged/accolade/milestone]")
        type_choice = input("Type: ").strip().lower()

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

        print(f"Activity history for student {student_id} (type: {type_choice}):")
        for entry in history:
            print(entry)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


# Student command to search activity history by type and id
@student_cli.command("searchHistory", help="Search activity history by type and id (interactive)")
def searchHistory():
    print("\n")
    try:
        print("Select type to search: [activity/student/request/logged/accolade/milestone/all]")
        type_choice = input("Type: ").strip().lower()

        # Search by activity id does not need a student id
        if type_choice in ("activity", "act"):
            activity_id = int(input("Enter activity history ID: "))
            result = search_history_by_activity(activity_id)
            if not result:
                print(f"No activity history found for activity id {activity_id}.")
                return
            for entry in result:
                print(entry)
            return

        # For types that require a student id, prompt for it now
        student_id = int(input("Enter your student ID: "))

        if type_choice in ("all",):
            result = search_history_by_student(student_id)
            if not result:
                print(f"No activity history found for student {student_id}.")
                return
            for entry in result:
                print(entry)
            return

        if type_choice in ("request", "requests"):
            req_id = int(input("Enter request ID: "))
            result = search_history_by_request(student_id, req_id)
        elif type_choice in ("logged", "loggedhours"):
            lh_id = int(input("Enter logged hours ID: "))
            result = search_history_by_logged_hours(student_id, lh_id)
        elif type_choice in ("accolade", "accolades"):
            ac_id = int(input("Enter accolade history ID: "))
            result = search_history_by_accolade(student_id, ac_id)
        elif type_choice in ("milestone", "milestones"):
            ms_id = int(input("Enter milestone history ID: "))
            result = search_history_by_milestone(student_id, ms_id)
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




'''STAFF COMMANDS'''

staff_cli = AppGroup('staff', help='Staff object commands')

#Command to create a new staff member (name, email)
@staff_cli.command("create", help="Create a new staff member")
def create_staff():
    print("\n")
    try:
        name = input("Enter staff name: ")
        email = input("Enter staff email: ")
        if "@" not in email:
            raise ValueError("Invalid email address.")
        password = input("Enter staff password: ")  
        staff = register_staff(name, email, password)

        print(f"Created staff member: {staff}")

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


#Command to the update staff member's attributes (username, email, password)
@staff_cli.command("update", help="Update a staff member's attributes via options")
@click.option("--staff_id", required=True, type=int, help="ID of the staff member to update.")
@click.option("--username", default=None, help="New username for the staff member.")
@click.option("--email", default=None, help="New email for the staff member.")
@click.option("--password", default=None, help="New password for the staff member.")
@with_appcontext
def update_staff_command(staff_id, username, email, password):
    
    if not username and not email and not password:
        click.echo("Error: At least one attribute (--username, --email, or --password) must be provided.")
        return
    
    try:
        staff = update_staff(staff_id, username, email, password)
        
        if staff:
            click.echo(f"Successfully updated Staff ID {staff.staff_id}: {staff.username}")
        else:
            click.echo(f"Error: Staff with ID {staff_id} not found.")

    except ValueError as e:
        click.echo(f"Update failed: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred during update: {e}", err=True)
        sys.exit(1)
 
 
#Command to create a new accolade (staff_id, description) 
@staff_cli.command("createAccolade", help="Creates a new accolade")
@click.option("--staff_id", required=True, type=int, help="ID of the staff member creating the accolade")
@click.option("--description", required=True, help="Description of the accolade")
@with_appcontext
def create_accolade_command(staff_id, description):
    from App.controllers.staff_controller import create_accolade
    
    accolade, error = create_accolade(staff_id, description)
    
    if error:
        click.echo(f"Error: {error}")
        return
    
    click.echo(f"Accolade created successfully!")
    click.echo(f"ID: {accolade.id}")
    click.echo(f"Description: '{description}'")
    click.echo(f"Created by Staff ID: {staff_id}")


#Command to update an accolade's attributes (staff_id, description)
@staff_cli.command("updateAccolade", help="Updates an accolade's attributes")
@click.option("--accolade_id", required=True, type=int, help="ID of the accolade to update")
@click.option("--staff_id", default=None, type=int, help="New staff ID")
@click.option("--description", default=None, type=str, help="New description")
@with_appcontext
def update_accolade_command(accolade_id, staff_id, description):
      
    if staff_id is None and description is None:
        click.echo("Error: At least one attribute (--staff_id or --description) must be provided.")
        return

    try:
        result, error = update_accolade(accolade_id, staff_id=staff_id, description=description)

        if error:
            click.echo(f"Error: {error}")
            return

        accolade = result.get('accolade')
        click.echo("Accolade updated successfully!")
        click.echo(f"ID: {accolade.id}")
        click.echo("Updated fields:")
        for field in result.get('updated_fields', []):
            click.echo(f"  - {field}")

    except ValueError as e:
        click.echo(f"Update failed: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred during update: {e}", err=True)
        sys.exit(1)
        

#Command to delete an accolade by its ID, with option to delete all history records
@staff_cli.command("deleteAccolade", help="Deletes an accolade by ID")
@click.argument("accolade_id", type=int)
@click.option("--delete_all_history", is_flag=True, help="Also delete all history records for this accolade")
def delete_accolade_command(accolade_id, delete_all_history):

    success, result = delete_accolade(accolade_id, delete_history=delete_all_history)
    
    if not success:
        click.echo(f"Error: {result}")
        return
    
    click.echo(f"Accolade deleted successfully!")
    click.echo(f"ID: {accolade_id}")
    click.echo(f"Description: '{result['description']}'")
    
    if delete_all_history:
        click.echo(f"History records deleted: {result['history_deleted']}")
        if result['empty_activities_deleted'] > 0:
            click.echo(f"Empty activity records cleaned up: {result['empty_activities_deleted']}")
    else:
        click.echo(f"History records preserved")
 

#Command to assign a student to an accolade (accolade_id, student_id, staff_id)    
@staff_cli.command("assignAccolade", help="Assigns a student to an accolade")
@click.option("--accolade_id", type=int, required=True, help="ID of the accolade")
@click.option("--student_id", type=int, required=True, help="ID of the student")
@click.option("--staff_id", type=int, required=True, help="ID of the staff member making the assignment")
def assign_accolade_command(accolade_id, student_id, staff_id):
  
    result, error = assign_accolade_to_student(accolade_id, student_id, staff_id)
    
    if error:
        click.echo(f"Error: {error}")
        return
    
    accolade = result['accolade']
    student = result['student']
    history = result['history']
    
    click.echo(f"Student assigned to accolade successfully!")
    click.echo(f"Accolade ID: {accolade.id}")
    click.echo(f"Description: '{accolade.description}'")
    click.echo(f"Student ID: {student.student_id}")
    click.echo(f"Assigned by Staff ID: {staff_id}")
    click.echo(f"History Record ID: {history.id}")
    click.echo(f"Timestamp: {history.timestamp}")
    
 
#Command to remove a student from an accolade (accolade_id, student_id, delete_history) 
@staff_cli.command("removeAccolade", help="Removes a student from an accolade")
@click.option("--accolade_id", type=int, required=True, help="ID of the accolade")
@click.option("--student_id", type=int, required=True, help="ID of the student")
@click.option("--delete_history", is_flag=True, help="Also delete the history record for this assignment")
def remove_accolade_command(accolade_id, student_id, delete_history):
    
    result, error = remove_accolade_from_student(accolade_id, student_id, delete_history=delete_history)
    
    if error:
        click.echo(f"Error: {error}")
        return
    
    accolade = result['accolade']
    student = result['student']
    
    click.echo(f"Student removed from accolade successfully!")
    click.echo(f"Accolade ID: {accolade.id}")
    click.echo(f"Description: '{accolade.description}'")
    click.echo(f"Student ID: {student.student_id}")
    
    if delete_history:
        if result['history_deleted'] > 0:
            click.echo(f" History record deleted: Yes")
            if result['activity_deleted']:
                click.echo(f"Empty activity record cleaned up: Yes")
        else:
            click.echo(f"History record deleted: None found")
    else:
        click.echo(f"History record preserved")
        
          
#Command for staff to view all pending requests
@staff_cli.command("requests", help="View all pending hour requests")
def requests():
    try:
        pending_requests = fetch_all_requests()
        if not pending_requests:
            print("No pending requests found.")
            return
        
        print("\n\nPending Requests:")
        for req in pending_requests:
            print(f"Request ID: {req['id']:<4} "
                  f"Student: {req['student_name']:<10} "
                  f"Hours: {req['hours']:<7} \t"
                  f" Status: {req['status']}")
    
        print("\n")

    except Exception as e:
        print(f"An error occurred while fetching requests: {e}")


#Command for staff to approve a student's request (staff_id, request_id)
#Once approved it is added to logged hours database
@staff_cli.command("approveRequest", help="Staff approves a student's request")
def approveRequest():
    print("\n")
    try:
        staff_id = int(input("Enter your staff ID: "))
        request_id = int(input("Enter the request ID to approve: "))

        results = process_request_approval(staff_id,request_id)
    
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
@staff_cli.command("denyRequest", help="Staff denies a student's request") 
def denyRequest():
    print("\n")
    try:
        staff_id = int(input("Enter your staff ID: "))
        request_id = int(input("Enter the request ID to deny: "))

        results = process_request_denial(staff_id,request_id)

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

# Command to search staff by field (name, email, or ID)
@staff_cli.command("search", help="Search for a staff member by name, email, or ID")
@click.argument("query")
def search_staff(query):
    print("\n")
    try:
        staff = staff_query_router(query)
        print(f"Found staff member: {staff}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# Command to delete a staff member by id (staff_id)
@staff_cli.command("delete", help="Delete a staff member by ID")
def delete_staff_command():
    staff_id = int(input("Enter the staff ID to delete: "))
    try:
        delete_staff(staff_id)
        print(f"Staff member with ID {staff_id} has been deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to delete ALL staff members (for testing purposes)
@staff_cli.command("deleteAll", help="Delete ALL staff members (testing purposes only)")
def delete_all_staff_command():
    confirmation = input("\033[91m\033[5m⚠️  Are you sure you want to delete ALL staff members? This action cannot be undone. (yes/no): ⚠️\033[0m ")
    if confirmation.lower() == 'yes':
        try:
            print("Nuking all staff members... 💣")
            num_deleted = Staff.query.delete()
            db.session.commit()
            print(f"All {num_deleted} staff members are gone. 💥")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
    else:
        print("Operation cancelled.")

# Command to update a staff member's information (staff_id, name, email, password) via CLI options
@staff_cli.command("update", help="Update a staff member's information")
@click.argument("staff_id", type=int)
@click.option("--name", default=None, help="New name for the staff member")
@click.option("--email", default=None, help="New email for the staff member")
@click.option("--password", default=None, help="New password for the staff member")
def update_staff_command(staff_id, name, email, password):
    print("\n")
    try:
        updated_staff = update_staff_info(
            staff_id,
            name if name else None,
            email if email else None,
            password if password else None
        )
        print(f"Updated staff member: {updated_staff}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(staff_cli) # add the group to the cli




'''REQUEST COMMANDS'''



request_cli = AppGroup('request', help='Request object commands')

# Command to delete a request by ID
@request_cli.command("delete", help="Delete a service hour request by ID")
def delete_request():
    print("\n")
    try:
        request_id = int(input("Enter the request ID to delete: ")) 
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

@request_cli.command("update", help="Update a request's attributes (student_id, service, hours, status)")
@click.option("--request_id", required=True, type=int, help="ID of the request to update")
@click.option("--student_id", default=None, type=int, help="New Student ID")
@click.option("--service", default=None, help="New Service description")
@click.option("--hours", default=None, type=float, help="New Hours value")
@click.option("--status", default=None, help="New Status (Pending/Approved/Denied)")
@with_appcontext
def update_request_command(request_id, student_id, service, hours, status):

    if not student_id and not service and not hours and not status:
        click.echo("Error: At least one attribute (--student_id, --service, --hours, --status) must be provided.")
        return

    try:
        request, message = update_request_entry(request_id, student_id, service, hours, status)

        if request:
            click.echo(f"Successfully updated Request ID {request.id}: {message}")
        else:
            click.echo(f"Error: {message}")

    except ValueError as e:
        click.echo(f"Update failed: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred during update: {e}", err=True)
        sys.exit(1)



# Command to search requests by student_id, service, or date
@request_cli.command("search", help="Search requests by student_id, service, or date_completed")
@click.option("--student_id", default=None, type=int, help="Student ID to filter requests")
@click.option("--service", default=None, type=str, help="Service description to search for")
@click.option("--date", default=None, type=str, help="Date completed (YYYY-MM-DD) to filter requests")
@with_appcontext
def search_request_command(student_id, service, date):
    

    if student_id is None and service is None and date is None:
        click.echo("Error: At least one search criterion (--student_id, --service, or --date) must be provided.")
        return
    
    try:
        requests, error = search_requests(student_id=student_id, service=service, date=date)
        
        if error:
            click.echo(f"Error: {error}")
            return

        if not requests:
            click.echo("No requests found matching the criteria.")
            return
        
        click.echo(f"\nFound {len(requests)} request(s):")
        click.echo("-" * 120)
        for req in requests:
            student = Student.query.get(req.student_id)
            student_name = student.username if student else "Unknown"
            click.echo(f"Request ID: {req.id:<4} | Student: {student_name:<15} | Service: {req.service:<25} | Hours: {req.hours:<6} | Status: {req.status:<10} | Date: {req.date_completed.date()}")
        click.echo("-" * 120)
        
    except Exception as e:
        click.echo(f"An error occurred during search: {e}", err=True)


#Command to drop request table (all request records and associated activity records)
@request_cli.command("dropRequestTable", help="Drops all request records from the database (WARNING: IRREVERSIBLE)")
@click.confirmation_option(prompt="Are you sure you want to delete ALL request records? This cannot be undone")
@with_appcontext
def drop_request_table_command():
    try:
        result, error = drop_request_table()
        
        if error:
            click.echo(f"Error: {error}", err=True)
            return
        
        click.echo(f"Request table dropped successfully!")
        click.echo(f"Requests deleted: {result['requests_deleted']}")
        click.echo(f"Associated activity records cleaned up")
        click.echo(f"\nAll request records have been permanently removed from the database.")
        
    except Exception as e:
        click.echo(f"An error occurred during drop operation: {e}", err=True)
        sys.exit(1)
        
        
app.cli.add_command(request_cli) 



'''ACCOLADE COMMANDS'''



accolade_cli = AppGroup('accolade', help='Accolade search commands')

#Command to search accolades by id, staff_id, description, or student_id
@accolade_cli.command("search", help="Search accolades by id, staff_id, description, or student_id")
@click.option("--accolade_id", default=None, type=int, help="Accolade ID to search for")
@click.option("--staff_id", default=None, type=int, help="Staff ID who created the accolade")
@click.option("--description", default=None, type=str, help="Text to match in accolade description")
@click.option("--student_id", default=None, type=int, help="Student ID to filter accolades for")
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
            click.echo(f"Error: {error}")
            return

        if not accolades:
            click.echo("No accolades found matching the criteria.")
            return

        click.echo(f"Found {len(accolades)} accolade(s):")
        for accolade in accolades:
            click.echo(f"Accolade ID: {accolade.id}")
            click.echo(f"Description: '{accolade.description}'")
            click.echo(f"Created by Staff ID: {accolade.staff_id}")
            click.echo(f"Number of students: {len(accolade.students)}")
            if accolade.students:
                student_ids = [s.student_id for s in accolade.students]
                click.echo(f"Student IDs: {', '.join(map(str, student_ids))}")
            click.echo()

    except Exception as e:
        click.echo(f"An error occurred during search: {e}", err=True)


#Command to drop accolade table (all accolade records and student-accolade associations)
@accolade_cli.command("dropAccoladeTable", help="Drops all accolade records from the database (WARNING: IRREVERSIBLE)")
@click.confirmation_option(prompt="Are you sure you want to delete ALL accolade records? This cannot be undone")
@with_appcontext
def drop_accolade_table_command():
    try:
        result, error = drop_accolade_table()
        
        if error:
            click.echo(f"Error: {error}", err=True)
            return
        
        click.echo(f"Accolade table dropped successfully!")
        click.echo(f"Accolades deleted: {result['accolades_deleted']}")
        click.echo(f"Student-accolade associations cleared")
        click.echo(f"History records preserved")
        click.echo(f"\nAll accolade records have been permanently removed from the database.")
        
    except Exception as e:
        click.echo(f"An error occurred during drop operation: {e}", err=True)
        sys.exit(1)

app.cli.add_command(accolade_cli)


# '''
# Test Commands
# '''

# test = AppGroup('test', help='Testing commands') 

# @test.command("unit", help="Run User tests")
# def unit_tests_command():
    
#     sys.exit(pytest.main(["-k", "UserUnitTests or StudentUnitTests or StaffUnitTests or RequestUnitTests or LoggedHoursUnitTests"]))
    
# app.cli.add_command(test)

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

# Command to create a logged hours entry
@app.cli.command("createLoggedHours", help="Create a logged hours entry")
@click.argument("student_id", type=int)
@click.argument("staff_id", type=int)
@click.argument("hours", type=float)
@click.option("--status", default="approved", help="Status for the logged hours (default: approved)")
@click.option("--service", default=None, help="Service description for the logged hours (optional)")
@click.option("--timestamp", default=datetime.utcnow(), help="Timestamp for the logged hours (optional, format: YYYY-MM-DD HH:MM:SS)")
def create_logged_hours_command(student_id, staff_id, hours, status, service, timestamp):
    print("\n")
    try:
        log = create_logged_hours(student_id, staff_id, hours, status, service, timestamp)
        print(f"Created logged hours entry: {log}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

# Command to delete a logged hours entry by ID
@app.cli.command("deleteLoggedHours", help="Delete a logged hours entry by ID")
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
@app.cli.command("deleteAllLoggedHours", help="Delete ALL logged hours entries (testing purposes only)")
def delete_all_logged_hours_command():
    confirmation = input("\033[91m\033[5m⚠️ Are you sure you want to delete ALL logged hours entries? This action cannot be undone. (yes/no): ")
    if confirmation.lower() == 'yes':
        try:
            print ("Nuking all logged hours entries... 💣")
            num_deleted = delete_all_logged_hours()
            print(f"All {num_deleted} logged hours entries have been deleted. 💥")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Operation cancelled.")
        
# Define regex patterns for date and date range detection        
RANGE_PATTERN = r"^\d{4}-\d{2}-\d{2}:\d{4}-\d{2}-\d{2}$"
DATE_PATTERN  = r"^\d{4}-\d{2}-\d{2}$"

def detect_query_type(query):
    # Student ID
    if query.isdigit() and query.startswith("8160") and len(query) == 9: # Assuming student IDs start with '8160' and are 9 digits long, this can be adjusted as needed
        return "student_id"

    # Staff ID
    if query.isdigit() and query.startswith("3") and len(query) == 9: # Assuming staff IDs start with '3', this can be adjusted as needed
        return "staff_id"

    # Date range
    if re.match(RANGE_PATTERN, query):
        start_str, end_str = query.split(":")
        datetime.strptime(start_str, "%Y-%m-%d")
        datetime.strptime(end_str, "%Y-%m-%d")
        return "date_range"

    # Single date
    if re.match(DATE_PATTERN, query):
        datetime.strptime(query, "%Y-%m-%d")
        return "date"

    # Fallback: treat as service string
    return "service"

# Command to search logged hours by student-id, staff-id, or date
@app.cli.command("searchLoggedHours", help="Search logged hours by student-id, staff-id, date or service string. Dates follow YYYY-MM-DD format. Date ranges use YYYY-MM-DD:YYYY-MM-DD format.")
@click.argument("query")
def search_logged_hours_command(query):
    search_type = detect_query_type(query)
    try:
        results = search_logged_hours(query, search_type)
        if not results:
            print(f"No logged hours entries found for {search_type} '{query}'.")
            return
        print(f"Logged hours entries for {search_type} '{query}':")
        for log in results:
            print(log)
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to update a logged hours entry by ID
@app.cli.command("updateLoggedHours", help="Update a logged hours entry by ID")
@click.argument("log_id")
@click.option("--student_id", type=int, default=None, help="New student ID")
@click.option("--staff_id", type=int, default=None, help="New staff ID")
@click.option("--hours", type=float, default=None, help="New hours")
@click.option("--status", type=str, default=None, help="New status")

def update_logged_hours_command(log_id, student_id, staff_id, hours, status):
    print("\n")
    try:
        log = LoggedHoursHistory.query.get(int(log_id))
        if not log:
            print(f"LoggedHoursHistory entry with id {log_id} not found.")
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
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")
    
## LEADERBOARD COMMANDS ##
@app.cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard(): #Duplicate entry fixed, this is the correct one. I deleted the old duplicates.
    print("\n")
    try:
        leaderboard = generate_leaderboard() #reuse existing function from student controller

        print("Leaderboard (by approved hours):")
        if not leaderboard:
            print("No students found or hour data found.")
            return
        for rank, data in enumerate(leaderboard, 1):
            #Use rich table formatting for better CLI display
            print(f"{rank:<6}. {data['name']:<10} ------ \t{data['hours']} hours")
            
    except Exception as e:
        print(f"An error occurred while generating the leaderboard: {e}")
        
@app.cli.command("searchLeaderboard", help="Search leaderboard for a specific student by name or ID")
@click.argument("query")
def searchLeaderboard(query):
    print("\n")
    try:
        leaderboard = generate_leaderboard() #reuse existing function from student controller

        print(f"Searching leaderboard for '{query}':")
        if not leaderboard:
            print("No students found or hour data found.")
            return
        found = False
        for rank, data in enumerate(leaderboard, 1):
            if query.lower() in data['name'].lower() or query == str(data['student_id']):
                print(f"{rank:<6}. {data['name']:<10} ------ \t{data['hours']} hours")
                found = True
        if not found:
            print(f"No matching student found in the leaderboard for '{query}'.")
    except Exception as e:
        print(f"An error occurred while searching the leaderboard: {e}")