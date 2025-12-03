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
    pending_requests = RequestHistory.query.filter_by(status='Pending').count()
    total_students = Student.query.count()
    total_logged_hours = LoggedHoursHistory.query.count()
    from App.models import Accolade
    total_accolades = Accolade.query.count()

    return render_template('staff_main_menu.html',
                         staff=staff,
                         pending_requests=pending_requests,
                         total_students=total_students,
                         total_logged_hours=total_logged_hours,
                         total_accolades=total_accolades)

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

    return render_template('staff_milestones.html', milestones=milestones)

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
    
    return render_template('staff_create_milestone.html')

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