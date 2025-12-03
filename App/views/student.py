from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, RequestHistory, User
from App.database import db
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

    return render_template('student_main_menu.html',
                         student=student,
                         total_hours=total_hours,
                         pending_requests=pending_requests,
                         milestones_count=milestones_count,
                         accolades_count=accolades_count)

@student_views.route('/student/make-request', methods=['GET'])
@jwt_required()
def student_make_request():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')
    return render_template('message.html', title="Make Request", message="Make Request page - Coming Soon!")

@student_views.route('/student/stats', methods=['GET'])
@jwt_required()
def student_stats():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')
    return render_template('message.html', title="View Stats", message="View Stats page - Coming Soon!")

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

    return render_template('student_profile.html',
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
            return redirect(request.url)

        if not user.check_password(password):
            flash('Incorrect password')
            return redirect(request.url)

        if len(new_username) < 3 or len(new_username) > 20:
            flash('Username must be 3-20 characters long')
            return redirect(request.url)

        # Check if username already exists
        existing = User.query.filter_by(username=new_username).first()
        if existing:
            flash('Username already taken')
            return redirect(request.url)

        # Update username
        user.username = new_username
        db.session.commit()
        flash('Username changed successfully')
        return redirect('/student/profile')

    return render_template('student_change_username.html', student=student)

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
            return redirect(request.url)

        if new_email != confirm_email:
            flash('Email addresses do not match')
            return redirect(request.url)

        if "@" not in new_email:
            flash('Invalid email address')
            return redirect(request.url)

        if not user.check_password(password):
            flash('Incorrect password')
            return redirect(request.url)

        # Check if email already exists
        existing = User.query.filter_by(email=new_email).first()
        if existing:
            flash('Email already in use')
            return redirect(request.url)

        # Update email
        user.email = new_email
        db.session.commit()
        flash('Email changed successfully')
        return redirect('/student/profile')

    return render_template('student_change_email.html', student=student)

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
            return redirect(request.url)

        if not user.check_password(current_password):
            flash('Current password is incorrect')
            return redirect(request.url)

        if new_password != confirm_password:
            flash('New passwords do not match')
            return redirect(request.url)

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(request.url)

        # Basic password requirements check
        import re
        if not re.search(r'[A-Z]', new_password):
            flash('Password must contain at least one uppercase letter')
            return redirect(request.url)
        if not re.search(r'[a-z]', new_password):
            flash('Password must contain at least one lowercase letter')
            return redirect(request.url)
        if not re.search(r'\d', new_password):
            flash('Password must contain at least one number')
            return redirect(request.url)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            flash('Password must contain at least one special character')
            return redirect(request.url)

        # Update password
        user.set_password(new_password)
        db.session.commit()
        flash('Password changed successfully')
        return redirect('/student/profile')

    return render_template('student_change_password.html', student=student)

@student_views.route('/student/leaderboard', methods=['GET'])
@jwt_required()
def student_leaderboard():
    user = jwt_current_user
    if user.role != 'student':
        flash('Access forbidden: Not a student')
        return redirect('/login')
    return render_template('message.html', title="Leaderboard", message="Leaderboard page - Coming Soon!")

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