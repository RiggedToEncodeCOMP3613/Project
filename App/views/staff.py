from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student,Request
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request
from App.controllers.staff_controller import process_request_approval,process_request_denial

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
    req = Request.query.get(data['request_id'])
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
    req = Request.query.get(data['request_id'])
    if not req:
        return jsonify(message='Request not found'), 404    
    process_request_denial(user.staff_id, data['request_id'])
    return jsonify(message='Request denied'), 200