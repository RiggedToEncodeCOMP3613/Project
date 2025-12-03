from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, RequestHistory
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