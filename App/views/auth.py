from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views

from App.controllers import (
    login,
)
from App.models import User

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''

@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    username_or_email = data['username']
    selected_role = data.get('role')
    token = login(username_or_email, data['password'])
    if not token:
        flash('Invalid Username/Email or Password')
        return redirect('/login')

    # Get user to determine redirect based on role
    if "@" in username_or_email:
        user = User.query.filter_by(email=username_or_email).first()
    else:
        user = User.query.filter_by(username=username_or_email).first()

    # Check if selected role matches user's role
    if user.role != selected_role:
        flash('Invalid Username/Email or Password')
        return redirect('/login')

    if user.role == 'student':
        response = redirect('/student/main')
    elif user.role == 'staff':
        response = redirect('/staff/main')  # We'll need to create this later
    else:
        response = redirect('/')

    flash('Login Successful')
    remember = request.form.get('remember')
    if remember:
        set_access_cookies(response, token, max_age=2592000)  # 30 days
    else:
        set_access_cookies(response, token)
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect('/login')
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot_password.html')

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='Invalid Username/Email or Password'), 401
  response = jsonify(access_token=token)
  remember = data.get('remember')
  if remember:
    set_access_cookies(response, token, max_age=2592000)  # 30 days
  else:
    set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.user_id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response