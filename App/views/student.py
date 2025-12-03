from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, Staff, RequestHistory, User
from App.database import db
from App.controllers.leaderboard_controller import generate_leaderboard
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request

student_views = Blueprint('student_views', __name__, template_folder='../templates')

@student_views.route('/student/main', methods=['GET'])
@jwt_required()
def student_main_menu():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    # Get stats
    total_hours = student.total_hours
    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').count()
    milestones_count = len(student.check_for_milestones())
    accolades_count = len(student.check_accolades())

    return render_template('student/main_menu.html',
                          student=student,
                          total_hours=total_hours,
                          pending_requests=pending_requests,
                          milestones_count=milestones_count,
                          accolades_count=accolades_count)

@student_views.route('/student/make-request', methods=['GET', 'POST'])
@jwt_required()
def student_make_request():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')
    
    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')
    
    if request.method == 'POST':
        try:
            # Get form data
            service = request.form.get('service')
            date_completed = request.form.get('date')
            hours = request.form.get('hours')
            student_id = request.form.get('student_id')
            supervisor_id = request.form.get('supervisor_id')
            
            # Validate required fields
            if not all([service, date_completed, hours, student_id, supervisor_id]):
                flash('All fields are required.', 'error')
                return redirect(url_for('student_views.student_make_request'))
            
            # Import the create_request controller function
            from App.controllers.request_controller import create_request
            
            # Create the request
            req, message = create_request(
                student_id=int(student_id),
                service=service,
                staff_id=int(supervisor_id),
                hours=float(hours),
                date_completed=date_completed
            )
            
            if req is None:
                flash(f'Error: {message}', 'error')
                return redirect(url_for('student_views.student_make_request'))
            
            flash('Request created successfully!', 'success')
            return redirect(url_for('student_views.student_make_request'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
            return redirect(url_for('student_views.student_make_request'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('student_views.student_make_request'))
    
    # GET method
    staff_members = Staff.query.all()
    return render_template('student/make_request.html', 
                          student=student, 
                          staff_members=staff_members)

@student_views.route('/student/stats', methods=['GET'])
@jwt_required()
def student_stats():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').count()

    return render_template('student/view_stats_menu.html', pending_requests=pending_requests)

@student_views.route('/student/stats/accolades', methods=['GET'])
@jwt_required()
def student_stats_accolades():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    total_hours = student.total_hours
    
    # Fetch actual milestones from database
    from App.models import Milestone
    milestones = Milestone.query.order_by(Milestone.hours).all()
    milestone_hours = [m.hours for m in milestones]
    
    # Find next milestone
    next_milestone = next((m for m in milestone_hours if m > total_hours), None)
    accolades = student.check_accolades()

    return render_template('student/all_stats.html', student=student, total_hours=total_hours, next_milestone=next_milestone, accolades=accolades, milestones=milestones)

@student_views.route('/student/stats/pending', methods=['GET'])
@jwt_required()
def student_stats_pending():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').all()

    return render_template('student/pending_requests.html', requests=pending_requests)

@student_views.route('/student/stats/history', methods=['GET'])
@jwt_required()
def student_stats_history():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    requests = RequestHistory.query.filter(RequestHistory.student_id == user.student_id, RequestHistory.status != 'Pending').all()

    return render_template('student/request_history.html', requests=requests)

@student_views.route('/student/profile', methods=['GET'])
@jwt_required()
def student_profile():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    # Get stats
    total_hours = student.total_hours
    milestones_count = len(student.check_for_milestones())
    accolades_count = len(student.check_accolades())

    return render_template('student/profile.html',
                          student=student,
                          total_hours=total_hours,
                          milestones_count=milestones_count,
                          accolades_count=accolades_count)

@student_views.route('/student/change-username', methods=['GET', 'POST'])
@jwt_required()
def student_change_username():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    if request.method == 'POST':
        new_username = request.form.get('new_username')
        password = request.form.get('password')

        if not new_username or not password:
            flash('All fields are required')
            return redirect(url_for('student_views.student_change_username'))

        if not user.check_password(password):
            flash('Incorrect password')
            return redirect(url_for('student_views.student_change_email'))

        if len(new_username) < 3 or len(new_username) > 20:
            flash('Username must be 3-20 characters long')
            return redirect(url_for('student_views.student_change_username'))

        # Check if username already exists
        existing = User.query.filter_by(username=new_username).first()
        if existing:
            flash('Username already taken')
            return redirect(url_for('student_views.student_change_username'))

        # Update username
        user.username = new_username
        db.session.commit()
        flash('Username changed successfully')
        return redirect('/student/profile')

    return render_template('student/change_username.html', student=student)

@student_views.route('/student/change-email', methods=['GET', 'POST'])
@jwt_required()
def student_change_email():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    if request.method == 'POST':
        new_email = request.form.get('new_email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')

        if not new_email or not confirm_email or not password:
            flash('All fields are required')
            return redirect(url_for('student_views.student_change_email'))

        if new_email != confirm_email:
            flash('Email addresses do not match')
            return redirect(url_for('student_views.student_change_email'))

        if "@" not in new_email:
            flash('Invalid email address')
            return redirect(url_for('student_views.student_change_email'))

        if not user.check_password(password):
            flash('Incorrect password')
            return redirect(url_for('student_views.student_change_username'))

        # Check if email already exists
        existing = User.query.filter_by(email=new_email).first()
        if existing:
            flash('Email already in use')
            return redirect(url_for('student_views.student_change_email'))

        # Update email
        user.email = new_email
        db.session.commit()
        flash('Email changed successfully')
        return redirect('/student/profile')

    return render_template('student/change_email.html', student=student)

@student_views.route('/student/change-password', methods=['GET', 'POST'])
@jwt_required()
def student_change_password():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_password or not new_password or not confirm_password:
            flash('All fields are required')
            return redirect(url_for('student_views.student_change_password'))

        if not user.check_password(current_password):
            flash('Current password is incorrect')
            return redirect(url_for('student_views.student_change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match')
            return redirect(url_for('student_views.student_change_password'))

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('student_views.student_change_password'))

        # Basic password requirements check
        import re
        if not re.search(r'[A-Z]', new_password):
            flash('Password must contain at least one uppercase letter')
            return redirect(url_for('student_views.student_change_password'))
        if not re.search(r'[a-z]', new_password):
            flash('Password must contain at least one lowercase letter')
            return redirect(url_for('student_views.student_change_password'))
        if not re.search(r'\d', new_password):
            flash('Password must contain at least one number')
            return redirect(url_for('student_views.student_change_password'))
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            flash('Password must contain at least one special character')
            return redirect(url_for('student_views.student_change_password'))

        # Update password
        user.set_password(new_password)
        db.session.commit()
        flash('Password changed successfully')
        return redirect('/student/profile')

    return render_template('student/change_password.html', student=student)

@student_views.route('/student/leaderboard', methods=['GET'])
@jwt_required()
def student_leaderboard():
    user = jwt_current_user
    if user.role not in ['student', 'staff']:
        flash('Access forbidden')
        return redirect('/login')

    leaderboard = generate_leaderboard()

    return render_template('leaderboard.html', leaderboard=leaderboard, user_role=user.role)

@student_views.route('/api/accolades', methods=['GET'])
@jwt_required()
def accolades_report_action():
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    report = fetch_accolades(user.student_id)
    if not report:
        return jsonify(message='No accolades for this student'), 404
    return jsonify(report)

@student_views.route('/api/make_request', methods=['POST'])
@jwt_required()
def make_request_action():
    user = jwt_current_user
    if user.role != 'student':
        return jsonify(message='Access forbidden: Not a student'), 403
    data = request.json
    if not data or 'hours' not in data:
        return jsonify(message='Invalid request data'), 400
    request_2 = create_hours_request(user.student_id, data['hours'])
    return jsonify(request_2.get_json()), 201

@student_views.route('/api/students', methods=['GET'])
@jwt_required()
def get_students_action():
    return get_all_students_json()

@student_views.route('/view_menu', methods=['GET'])
@jwt_required()
def view_menu():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    # Get stats
    total_hours = student.total_hours
    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').count()
    milestones_count = len(student.check_for_milestones())
    accolades_count = len(student.check_accolades())

    return render_template('student/menu.html',
                          student=student,
                          total_hours=total_hours,
                          pending_requests=pending_requests,
                          milestones_count=milestones_count,
                          accolades_count=accolades_count)

@student_views.route('/make_request', methods=['GET', 'POST'])
@jwt_required()
def make_request():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    if request.method == 'POST':
        try:
            # Get form data
            service = request.form.get('service')
            date_completed = request.form.get('date')
            hours = request.form.get('hours')
            student_id = request.form.get('student_id')
            supervisor_id = request.form.get('supervisor_id')

            # Validate required fields
            if not all([service, date_completed, hours, student_id, supervisor_id]):
                flash('All fields are required.', 'error')
                return redirect(url_for('student_views.make_request'))

            # Create the request using create_request controller function
            from App.controllers.request_controller import create_request
            req, message = create_request(
                student_id=int(student_id),
                service=service,
                staff_id=int(supervisor_id),
                hours=float(hours),
                date_completed=date_completed
            )

            if req is None:
                flash(f'Error: {message}', 'error')
                return redirect(url_for('student_views.make_request'))

            flash('Request created successfully!', 'success')
            return redirect(url_for('student_views.make_request'))

        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
            return redirect(url_for('student_views.make_request'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('student_views.make_request'))

    # GET method
    staff_members = Staff.query.all()
    return render_template('student/make_request.html',
                          student=student,
                          staff_members=staff_members)

@student_views.route('/view_stats_menu', methods=['GET'])
@jwt_required()
def view_stats_menu():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    return render_template('student/view_stats_menu.html')

@student_views.route('/view_stats', methods=['GET'])
@jwt_required()
def view_stats():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    student = Student.query.get(user.student_id)
    if not student:
        flash('Student profile not found')
        return redirect('/login')

    total_hours = student.total_hours
    
    # Fetch actual milestones from database
    from App.models import Milestone
    milestones = Milestone.query.order_by(Milestone.hours).all()
    milestone_hours = [m.hours for m in milestones]
    
    # Find next milestone
    next_milestone = next((m for m in milestone_hours if m > total_hours), None)
    accolades = student.check_accolades()
    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').count()

    return render_template('student/all_stats.html', student=student, total_hours=total_hours, next_milestone=next_milestone, accolades=accolades, milestones=milestones, pending_requests=pending_requests)

@student_views.route('/view_pending_requests', methods=['GET'])
@jwt_required()
def view_pending_requests():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').all()

    return render_template('student/pending_requests.html', requests=pending_requests)

@student_views.route('/view_requests_history', methods=['GET'])
@jwt_required()
def view_requests_history():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')

    requests = RequestHistory.query.filter(RequestHistory.student_id == user.student_id, RequestHistory.status != 'Pending').all()

    return render_template('student/request_history.html', requests=requests)