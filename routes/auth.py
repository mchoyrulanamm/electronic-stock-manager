from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from routes.__init__ import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))

        flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        current = request.form.get('current_password', '')
        new = request.form.get('new_password', '')
        confirm = request.form.get('confirm_password', '')

        if not user.check_password(current):
            flash('Current password is incorrect', 'danger')
        elif len(new) < 4:
            flash('New password must be at least 4 characters', 'danger')
        elif new != confirm:
            flash('New passwords do not match', 'danger')
        else:
            user.set_password(new)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('index'))

    return render_template('auth/change_password.html')
