import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy.exc import IntegrityError

from application import db
from application.lib import request_input
from application.model import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        
        data = {
            "username": request_input("username"), 
            "password": request_input("password") 
        }
        
        error = None

        if not data.get("username"):
            error = 'Username is required.'
        elif not data.get("password"):
            error = 'Password is required.'

        if error is None:
            try:
                user = User(
                    username=data.get("username"), 
                    password=generate_password_hash(data.get("password")), 
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                error = f"User {data.get("username")} is already registered."
                db.session.rollback()
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        
        data = {
            "username": request_input("username"), 
            "password": request_input("password") 
        }
        error = None
        
        user = User.query.filter_by(username=data.get("username")).first()
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, data.get("password")):
            error = 'Incorrect password.'
            
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
