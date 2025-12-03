from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, RequestHistory, LoggedHoursHistory, Staff
from App.controllers.leaderboard_controller import generate_leaderboard
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request
from App.controllers.request_controller import process_request_approval, process_request_denial
from App import db

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/main', methods=['GET'])
@jwt_required()
def staff_main_menu():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    staff = Staff.query.get(user.staff_id)
    if not staff:
        flash('Staff profile not found')
        return redirect('/login')

    # Get some stats
    pending_requests = RequestHistory.query.filter_by(status='Pending', staff_id=user.staff_id).count()
    total_students = Student.query.count()
    total_logged_hours = LoggedHoursHistory.query.count()
    from App.models import Accolade
    total_accolades = Accolade.query.count()

    return render_template('staff/main_menu.html',
                         staff=staff,
                         pending_requests=pending_requests,
                         total_students=total_students,
                         total_logged_hours=total_logged_hours,
                         total_accolades=total_accolades)

@staff_views.route('/staff/pending-requests', methods=['GET'])
@jwt_required()
def staff_pending_requests():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    # Get all pending requests for this staff member
    pending_requests = RequestHistory.query.filter_by(status='Pending', staff_id=user.staff_id).all()
    
    # Get student information for each request
    requests_with_students = []
    for request in pending_requests:
        student = Student.query.get(request.student_id)
        requests_with_students.append({
            'request': request,
            'student': student
        })

    return render_template('staff/pending_requests.html', requests=requests_with_students)

# Redirect from /staff/log-hours to /staff/loghours for backward compatibility
@staff_views.route('/staff/log-hours', methods=['GET'])
@jwt_required()
def redirect_log_hours():
    return redirect('/staff/loghours')

@staff_views.route('/staff/milestones', methods=['GET'])
@jwt_required()
def staff_milestones():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    from App.models import Milestone, MilestoneHistory
    milestones = Milestone.query.order_by(Milestone.hours).all()
    
    # Count students who achieved each milestone
    for milestone in milestones:
        milestone.student_count = MilestoneHistory.query.filter_by(milestone_id=milestone.id).count()

    return render_template('staff/milestones.html', milestones=milestones)

@staff_views.route('/staff/delete-milestone/<int:milestone_id>', methods=['POST'])
@jwt_required()
def delete_milestone(milestone_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    from App.controllers.milestone_controller import delete_milestone as delete_milestone_controller
    from App.models import Milestone
    
    milestone = Milestone.query.get(milestone_id)
    if not milestone:
        flash('Milestone not found', 'error')
        return redirect('/staff/milestones')
    
    try:
        delete_milestone_controller(milestone_id, delete_history=True)
        flash(f'Milestone ({milestone.hours} hours) deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting milestone: {str(e)}', 'error')
    
    return redirect('/staff/milestones')

@staff_views.route('/staff/create-milestone', methods=['GET'])
@jwt_required()
def create_milestone_page():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    return render_template('staff/create_milestone.html')

@staff_views.route('/staff/create-milestone', methods=['POST'])
@jwt_required()
def create_milestone_submit():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    hours = request.form.get('hours')
    
    if not hours:
        flash('Hours field is required', 'error')
        return redirect('/staff/create-milestone')
    
    try:
        hours = int(hours)
        if hours <= 0:
            flash('Hours must be greater than 0', 'error')
            return redirect('/staff/create-milestone')
        
        from App.controllers.milestone_controller import create_milestone as create_milestone_controller
        from App.models import Milestone
        
        # Check if milestone already exists
        existing = Milestone.query.filter_by(hours=hours).first()
        if existing:
            flash(f'Milestone with {hours} hours already exists', 'error')
            return redirect('/staff/create-milestone')
        
        create_milestone_controller(hours)
        flash(f'Milestone ({hours} hours) created successfully', 'success')
        return redirect('/staff/milestones')
    
    except ValueError:
        flash('Hours must be a valid number', 'error')
        return redirect('/staff/create-milestone')
    except Exception as e:
        flash(f'Error creating milestone: {str(e)}', 'error')
        return redirect('/staff/create-milestone')

@staff_views.route('/staff/edit-milestone/<int:milestone_id>', methods=['GET'])
@jwt_required()
def edit_milestone_page(milestone_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    from App.models import Milestone
    milestone = Milestone.query.get(milestone_id)
    if not milestone:
        flash('Milestone not found', 'error')
        return redirect('/staff/milestones')
    
    return render_template('staff/edit_milestone.html', milestone=milestone)

@staff_views.route('/staff/edit-milestone/<int:milestone_id>', methods=['POST'])
@jwt_required()
def edit_milestone_submit(milestone_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    from App.models import Milestone
    milestone = Milestone.query.get(milestone_id)
    if not milestone:
        flash('Milestone not found', 'error')
        return redirect('/staff/milestones')
    
    hours = request.form.get('hours')
    
    if not hours:
        flash('Hours field is required', 'error')
        return redirect(f'/staff/edit-milestone/{milestone_id}')
    
    try:
        hours = int(hours)
        if hours <= 0:
            flash('Hours must be greater than 0', 'error')
            return redirect(f'/staff/edit-milestone/{milestone_id}')
        
        # Check if another milestone already has this hours value
        existing = Milestone.query.filter_by(hours=hours).filter(Milestone.id != milestone_id).first()
        if existing:
            flash(f'Milestone with {hours} hours already exists', 'error')
            return redirect(f'/staff/edit-milestone/{milestone_id}')
        
        from App.controllers.milestone_controller import update_milestone as update_milestone_controller
        update_milestone_controller(milestone_id, hours)
        flash(f'Milestone updated to {hours} hours successfully', 'success')
        return redirect('/staff/milestones')
    
    except ValueError:
        flash('Hours must be a valid number', 'error')
        return redirect(f'/staff/edit-milestone/{milestone_id}')
    except Exception as e:
        flash(f'Error updating milestone: {str(e)}', 'error')
        return redirect(f'/staff/edit-milestone/{milestone_id}')

@staff_views.route('/staff/accolades', methods=['GET'])
@jwt_required()
def staff_accolades():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    from App.models import Accolade, AccoladeHistory
    accolades = Accolade.query.all()
    
    # Count total students awarded and personally awarded for each accolade
    for accolade in accolades:
        accolade.total_count = AccoladeHistory.query.filter_by(accolade_id=accolade.id).count()
        accolade.personal_count = AccoladeHistory.query.filter_by(accolade_id=accolade.id, staff_id=user.staff_id).count()

    return render_template('staff/accolades.html', accolades=accolades)

@staff_views.route('/staff/create-accolade', methods=['GET'])
@jwt_required()
def create_accolade_page():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    return render_template('staff/create_accolade.html')

@staff_views.route('/staff/create-accolade', methods=['POST'])
@jwt_required()
def create_accolade_submit():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    description = request.form.get('description')
    
    if not description:
        flash('Accolade name field is required', 'error')
        return redirect('/staff/create-accolade')
    
    try:
        from App.controllers.accolade_controller import create_accolade as create_accolade_controller
        from App.models import Accolade
        
        # Check if accolade already exists
        existing = Accolade.query.filter_by(description=description).first()
        if existing:
            flash(f'Accolade "{description}" already exists', 'error')
            return redirect('/staff/create-accolade')
        
        accolade, error = create_accolade_controller(user.staff_id, description)
        if error:
            flash(error, 'error')
            return redirect('/staff/create-accolade')
        
        flash(f'Accolade "{description}" created successfully', 'success')
        return redirect('/staff/accolades')
    
    except Exception as e:
        flash(f'Error creating accolade: {str(e)}', 'error')
        return redirect('/staff/create-accolade')

@staff_views.route('/staff/edit-accolade/<int:accolade_id>', methods=['GET'])
@jwt_required()
def edit_accolade_page(accolade_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    from App.models import Accolade
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        flash('Accolade not found', 'error')
        return redirect('/staff/accolades')
    
    return render_template('staff/edit_accolade.html', accolade=accolade)

@staff_views.route('/staff/edit-accolade/<int:accolade_id>', methods=['POST'])
@jwt_required()
def edit_accolade_submit(accolade_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    from App.models import Accolade
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        flash('Accolade not found', 'error')
        return redirect('/staff/accolades')
    
    description = request.form.get('description')
    
    if not description:
        flash('Accolade name field is required', 'error')
        return redirect(f'/staff/edit-accolade/{accolade_id}')
    
    try:
        # Check if another accolade already has this description
        existing = Accolade.query.filter_by(description=description).filter(Accolade.id != accolade_id).first()
        if existing:
            flash(f'Accolade "{description}" already exists', 'error')
            return redirect(f'/staff/edit-accolade/{accolade_id}')
        
        from App.controllers.accolade_controller import update_accolade as update_accolade_controller
        result, error = update_accolade_controller(accolade_id, description=description)
        if error:
            flash(error, 'error')
            return redirect(f'/staff/edit-accolade/{accolade_id}')
        
        flash(f'Accolade updated successfully', 'success')
        return redirect('/staff/accolades')
    
    except Exception as e:
        flash(f'Error updating accolade: {str(e)}', 'error')
        return redirect(f'/staff/edit-accolade/{accolade_id}')

@staff_views.route('/staff/delete-accolade/<int:accolade_id>', methods=['POST'])
@jwt_required()
def delete_accolade(accolade_id):
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    from App.controllers.accolade_controller import delete_accolade as delete_accolade_controller
    from App.models import Accolade
    
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        flash('Accolade not found', 'error')
        return redirect('/staff/accolades')
    
    try:
        description = accolade.description
        delete_accolade_controller(accolade_id, delete_history=True)
        flash(f'Accolade "{description}" deleted successfully', 'success')
    except Exception as e:
        flash(f'Error deleting accolade: {str(e)}', 'error')
    
    return redirect('/staff/accolades')

@staff_views.route('/staff/award-accolade', methods=['GET'])
@jwt_required()
def award_accolade_page():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    from App.models import Student, Accolade, AccoladeHistory
    students = Student.query.all()
    accolades = Accolade.query.all()
    
    # Add accolade count and accolade list to each student
    for student in students:
        student_accolades = AccoladeHistory.query.filter_by(student_id=student.student_id).all()
        student.accolade_count = len(student_accolades)
        student.accolades = [accolade.description for accolade in Accolade.query.join(AccoladeHistory).filter(AccoladeHistory.student_id == student.student_id).all()]
    
    return render_template('staff/award_accolade.html', students=students, accolades=accolades)

@staff_views.route('/staff/award-accolade', methods=['POST'])
@jwt_required()
def award_accolade_submit():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')
    
    student_id = request.form.get('student_id')
    accolade_id = request.form.get('accolade_id')
    
    if not student_id or not accolade_id:
        flash('Please select both a student and an accolade', 'error')
        return redirect('/staff/award-accolade')
    
    try:
        student_id = int(student_id)
        accolade_id = int(accolade_id)
        
        from App.models import Student, Accolade, AccoladeHistory
        from App.controllers.accolade_controller import assign_accolade_to_student
        
        student = Student.query.get(student_id)
        if not student:
            flash('Student not found', 'error')
            return redirect('/staff/award-accolade')
        
        accolade = Accolade.query.get(accolade_id)
        if not accolade:
            flash('Accolade not found', 'error')
            return redirect('/staff/award-accolade')
        
        # Check if student already has this accolade
        existing = AccoladeHistory.query.filter_by(
            accolade_id=accolade_id,
            student_id=student_id
        ).first()
        if existing:
            flash(f'{student.username} already has the "{accolade.description}" accolade', 'error')
            return redirect('/staff/award-accolade')
        
        assign_accolade_to_student(accolade_id, student_id, user.staff_id)
        flash(f'Accolade "{accolade.description}" awarded to {student.username} successfully', 'success')
        return redirect('/staff/accolades')
    
    except ValueError:
        flash('Invalid student or accolade selection', 'error')
        return redirect('/staff/award-accolade')
    except Exception as e:
        flash(f'Error awarding accolade: {str(e)}', 'error')
        return redirect('/staff/award-accolade')

@staff_views.route('/staff/leaderboard', methods=['GET'])
@jwt_required()
def staff_leaderboard():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member')
        return redirect('/login')

    leaderboard = generate_leaderboard()

    return render_template('leaderboard.html', leaderboard=leaderboard, user_role=user.role)

@staff_views.route('/api/accept_request', methods=['PUT'])
@jwt_required()
def accept_request_action():
    user = jwt_current_user
    if user.role != 'staff':
        return jsonify(message='Access forbidden: Not a staff member'), 403
    data = request.json
    if not data or 'request_id' not in data:
        return jsonify(message='Invalid request data'), 400
    # Logic to accept the request goes here
    req = RequestHistory.query.get(data['request_id'])
    if not req:
        return jsonify(message='Request not found'), 404
    
    process_request_approval(user.staff_id, data['request_id'])
    
    return jsonify(message='Request accepted'), 200

@staff_views.route('/api/deny_request', methods=['PUT'])
@jwt_required()
def deny_request_action():
    user = jwt_current_user
    if user.role != 'staff':
        return jsonify(message='Access forbidden: Not a staff member'), 403
    data = request.json
    if not data or 'request_id' not in data:
        return jsonify(message='Invalid request data'), 400    
    # Logic to deny the request goes here
    req = RequestHistory.query.get(data['request_id'])
    if not req:
        return jsonify(message='Request not found'), 404    
    process_request_denial(user.staff_id, data['request_id'])
    return jsonify(message='Request denied'), 200

@staff_views.route('/api/delete_request', methods=['DELETE'])
@jwt_required()
def delete_request_action():
    user = jwt_current_user
    if user.role != 'staff':
        return jsonify(message='Access forbidden: Not a staff member'), 403
    data = request.json
    if not data or 'request_id' not in data:
        return jsonify(message='Invalid request data'), 400
    # Logic to delete the request goes here
    req = RequestHistory.query.get(data['request_id'])
    if not req:
        return jsonify(message='Request not found'), 404
    db.session.delete(req)
    db.session.commit()
    return jsonify(message='Request deleted'), 200

@staff_views.route('/api/delete_logs', methods=['DELETE'])
@jwt_required()
def delete_logs_action():
    user = jwt_current_user
    if user.role != 'staff':
        return jsonify(message='Access forbidden: Not a staff member'), 403
    # Logic to delete logs goes here
    data = request.json
    if not data or 'log_id' not in data:
        return jsonify(message='Invalid request data'), 400
    log = LoggedHoursHistory.query.get(data['log_id'])
    if not log:
        return jsonify(message='Log not found'), 404
    db.session.delete(log)
    db.session.commit()
    return jsonify(message='Logs deleted'), 200

@staff_views.route('/staff/loghours', methods=['GET', 'POST'])
@jwt_required()
def log_hours_view():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    
    # Import required modules for both GET and POST
    from datetime import datetime
    from pytz import utc
    from App.controllers.loggedHoursHistory_controller import create_logged_hours
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        hours = request.form.get('hours')
        if not student_id or not hours:
            flash('Student ID and hours are required', 'error')
            return redirect(url_for('staff_views.log_hours_view'))
        try:
            hours = float(hours)
        except ValueError:
            flash('Invalid hours value', 'error')
            return redirect(url_for('staff_views.log_hours_view'))
        student = Student.query.get(student_id)
        if not student:
            flash('Student not found', 'error')
            return redirect(url_for('staff_views.log_hours_view'))
        # Log the hours for the student
        create_logged_hours(student_id, user.staff_id, hours, service=request.form.get('service'), date_completed=utc.localize(datetime.utcnow()))
        flash('Hours logged successfully', 'success')
        return redirect(url_for('staff_views.log_hours_view'))
    
    # GET request - render the log hours page
    # Get all students for the dropdown
    students = Student.query.all()
    return render_template('staff/loghours.html', students=students)
    
@staff_views.route("/profile")
def profile_screen():
    return render_template("staff/profile.html", current_user=jwt_current_user)
    

@staff_views.route('/staff/change_username', methods=['GET', 'POST'])
@jwt_required()
def change_username_view():
    user = jwt_current_user
    print (user) #debug
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    if request.method == 'POST':
        print (request.form) #debug
        new_username = request.form.get('new_username')
        if not new_username:
            flash('New username is required', 'error')
            return redirect(url_for('staff_views.change_username_view'))
        try:
            existing_user = get_staff_by_name(new_username)
            if existing_user:
                flash('Username already taken', 'error')
                return redirect(url_for('staff_views.change_username_view'))
        except: # We actually want the try to fail, this indicates no user found with that name
            password = request.form.get('confirm_password')
            if not password or not user.check_password(password):
                flash('Incorrect password', 'error')
                return redirect(url_for('staff_views.change_username_view'))
            user.username = new_username
            db.session.commit()
            flash(f'Username changed successfully to {user.username}', 'success')
            print (f'Username changed successfully to {user.username}') #debug
            return redirect(url_for('staff_views.change_username_view'))
    # GET -> render the change username form
    return render_template('staff/change_username.html', current_user=user)

@staff_views.route('/staff/change_password', methods=['GET', 'POST'])
@jwt_required()
def change_password_view():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        if not current_password or not new_password:
            flash('Current and new passwords are required', 'error')
            return redirect(url_for('staff_views.change_password_view'))
        if not user.check_password(current_password):
            flash('Incorrect current password', 'error')
            return redirect(url_for('staff_views.change_password_view'))
        user.set_password(new_password)
        db.session.commit()
        flash(f'Password changed successfully to {new_password}, remember it!', 'success')
        return redirect(url_for('staff_views.change_password_view'))
    return render_template('staff/change_password.html', current_user=user)

@staff_views.route('/staff/change_email', methods=['GET', 'POST'])
@jwt_required()
def change_email_view():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    if request.method == 'POST':
        new_email = request.form.get('new_email')
        if not new_email:
            flash('New email is required', 'error')
            return redirect(url_for('staff_views.change_email_view'))
        existing_user = Staff.query.filter_by(email=new_email).first()
        if existing_user:
            flash('Email already in use', 'error')
            return redirect(url_for('staff_views.change_email_view'))
        password = request.form.get('confirm_password')
        if not password or not user.check_password(password):
            flash('Incorrect password', 'error')
            return redirect(url_for('staff_views.change_email_view'))
        user.email = new_email
        db.session.commit()
        flash(f'Email changed successfully to {new_email}', 'success')
        return redirect(url_for('staff_views.change_email_view'))
    # GET -> render change email form
    return render_template('staff/change_email.html', current_user=user)
    
@staff_views.route('/staff/profile', methods=['GET'])
@jwt_required()
def staff_profile_view():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    return render_template('staff/profile.html', current_user=user)

