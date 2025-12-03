from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student, Staff, RequestHistory, LoggedHoursHistory, AccoladeHistory, MilestoneHistory, ActivityHistory, User
from.index import index_views
from App.controllers.student_controller import get_all_students_json,fetch_accolades,create_hours_request
from App.controllers.request_controller import create_request, fetch_all_requests

student_page_views = Blueprint('student_page_views', __name__, template_folder='../templates')

@student_page_views.route('/view_menu', methods=['GET'])
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

@student_page_views.route('/make_request', methods=['GET', 'POST'])
def make_request():
    if request.method == 'GET':
        return render_template('student/make_request.html')
    
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
                return redirect(url_for('student_page_views.make_request'))
            
            # Create the request using create_request controller function
            req, message = create_request(
                student_id=int(student_id),
                service=service,
                staff_id=int(supervisor_id),
                hours=float(hours),
                date_completed=date_completed
            )
            
            if req is None:
                flash(f'Error: {message}', 'error')
                return redirect(url_for('student_page_views.make_request'))
            
            flash('Request created successfully!', 'success')
            return redirect(url_for('student_page_views.make_request'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'error')
            return redirect(url_for('student_page_views.make_request'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('student_page_views.make_request'))
        
@student_page_views.route('/view_stats_menu', methods=['GET'])
def view_stats_menu():
    if request.method == 'GET':
        return render_template('student/all_stats.html')

@student_page_views.route('/view_stats', methods=['GET'])
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

    pending_requests = RequestHistory.query.filter_by(student_id=user.student_id, status='Pending').count()

    return render_template('student/all_stats.html', student=student, pending_requests=pending_requests)

@student_page_views.route('/view_pending_requests', methods=['GET'])
def view_pending_requests():
    from App.models import RequestHistory
    pending_requests = RequestHistory.query.filter(RequestHistory.status == 'Pending').all()
    len_requests = len(pending_requests) if pending_requests else 0
    
    return render_template('student/pending_requests.html', requests=pending_requests, len=len_requests)

@student_page_views.route('/view_requests_history', methods=['GET'])
def view_requests_history():
    from App.models import RequestHistory
    requests = RequestHistory.query.filter(RequestHistory.status == 'Approved' or RequestHistory.status == 'Denied').all()
    len_requests = len(requests) if requests else 0
    
    return render_template('student/request_history.html', requests=requests, len=len_requests)
