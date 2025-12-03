from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, RequestHistory, LoggedHoursHistory, Staff
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
    pending_requests = RequestHistory.query.filter_by(status='Pending').count()
    total_students = Student.query.count()
    total_logged_hours = LoggedHoursHistory.query.count()

    return render_template('message.html', title="Staff Main Menu", message="Staff Main Menu - Coming Soon!")

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