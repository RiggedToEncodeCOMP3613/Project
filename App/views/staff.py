from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from pytz import utc
from App.controllers.staff_controller import get_staff_by_name
from App.models import Student, RequestHistory, LoggedHoursHistory
from App.models.staff import Staff
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request
from App.controllers.request_controller import process_request_approval, process_request_denial
from App.controllers.loggedHoursHistory_controller import *
from App import db

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

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

@staff_views.route('/staff/change_username', methods=['GET', 'POST'])
@jwt_required()
def change_username_view():
    user = jwt_current_user
    if user.role != 'staff':
        flash('Access forbidden: Not a staff member', 'error')
        return redirect(url_for('index_views.index'))
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        if not new_username:
            flash('New username is required', 'error')
            return redirect(url_for('staff_views.change_username_view'))
        existing_user = get_staff_by_name(new_username)
        if existing_user:
            flash('Username already taken', 'error')
            return redirect(url_for('staff_views.change_username_view'))
        password = request.form.get('password')
        if not password or not user.check_password(password):
            flash('Incorrect password', 'error')
            return redirect(url_for('staff_views.change_username_view'))
        user.username = new_username
        db.session.commit()
        flash('Username changed successfully', 'success')
        return redirect(url_for('staff_views.change_username_view'))

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
    return render_template('staff/changepassword.html', current_user=user)

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
        password = request.form.get('password')
        if not password or not user.check_password(password):
            flash('Incorrect password', 'error')
            return redirect(url_for('staff_views.change_email_view'))
        user.email = new_email
        db.session.commit()
        flash(f'Email changed successfully to {new_email}', 'success')
        return redirect(url_for('staff_views.change_email_view'))