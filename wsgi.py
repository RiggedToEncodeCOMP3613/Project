import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Student
from App.models import Staff
from App.models import Request
from App.main import create_app
from App.controllers.student_controller import delete_student, query_router, register_student, get_approved_hours, create_hours_request, fetch_requests, fetch_accolades, generate_leaderboard, update_student_info
from App.controllers.staff_controller import *
from App.controllers.app_controller import *
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
def search_student():
    print("\n")
    try:
        query = input("Enter student name, email, or ID: ")
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
    confirmation = input("Are you sure you want to delete ALL students? This action cannot be undone. (yes/no): ")
    if confirmation.lower() == 'yes':
        try:
            num_deleted = Student.query.delete()
            db.session.commit()
            print(f"All students have been deleted. Total deleted: {num_deleted}")
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
    else:
        print("Operation cancelled.")

#Command to update a student's information (student_id, name, email password) Use the function in student_controller.py
@student_cli.command("update", help="Update a student's information")
def update_student_command():
    print("\n")
    try:
        student_id = int(input("Enter the student ID to update: "))
        name = input("Enter new name (leave blank to keep current): ")
        email = input("Enter new email (leave blank to keep current): ")
        password = input("Enter new password (leave blank to keep current): ")

        updated_student = update_student_info(student_id, name if name else None, email if email else None, password if password else None)
        print(f"Updated student: {updated_student}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


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


#Student command to view leaderboard of students by approved hours
@student_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    print("\n")
    try:
        leaderboard = generate_leaderboard()

        print("Leaderboard (by approved hours):")
        if not leaderboard:
            print("No students found or hour data found.")
            return
        for rank, data in enumerate(leaderboard, 1):
            print(f"{rank:<6}. {data['name']:<10} ------ \t{data['hours']} hours")

    except Exception as e:
        print(f"An error occurred while generating the leaderboard: {e}")
    print("\n")

app.cli.add_command(student_cli) # add the group to the cli




'''STAFF COMMANDS'''



staff_cli = AppGroup('staff', help='Staff object commands')

#Command to create a new staff member (name, email)
@staff_cli.command("create", help="Create a new staff member")
def create_staff():
    print("\n")
    try:
        name = input("Enter staff name: ")
        email = input("Enter staff email: ")
        password = input("Enter staff password: ")  
        staff = register_staff(name, email, password)

        print(f"Created staff member: {staff}")

    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")


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


#staff command to view leaderboard of students by approved hours
@staff_cli.command("viewLeaderboard", help="View leaderboard of students by approved hours")
def viewLeaderboard():
    print("\n")
    try:
        leaderboard = generate_leaderboard()

        print("Leaderboard (by approved hours):")
        if not leaderboard:
            print("No students found or hour data found.")
            return
        for rank, data in enumerate(leaderboard, 1):
            print(f"{rank:<6}. {data['name']:<10} ------ \t{data['hours']} hours")

    except Exception as e:
        print(f"An error occurred while generating the leaderboard: {e}")
    print("\n")

# Command to search staff by field (name, email, or ID)
@staff_cli.command("search", help="Search for a staff member by name, email, or ID")
def search_staff():
    print("\n")
    try:
        query = input("Enter staff name, email, or ID: ")
        staff = query_router(query)  # Assuming a similar query_router exists for staff
        print(f"Found staff member: {staff}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n")

app.cli.add_command(staff_cli) # add the group to the cli



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