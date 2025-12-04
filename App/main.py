import os
from flask import Flask, render_template, redirect, url_for
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from App.database import init_db, create_db
from App.config import load_config


from App.controllers import (
    setup_jwt,
    add_auth_context,
    initialize
)

from App.views import views, setup_admin



def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    app.app_context().push()
    create_db()  # Create tables if they don't exist
    initialize(drop_first=False)
    jwt = setup_jwt(app)
    setup_admin(app)
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return redirect(url_for('auth_views.login_page'))

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return redirect(url_for('auth_views.login_page'))
    return app