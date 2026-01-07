from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main import main_bp
from app import db
import pytz


@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    timezones = pytz.common_timezones
    return render_template('profile.html', user=current_user, timezones=timezones)


@main_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    timezone = request.form.get('timezone')

    if not first_name or not last_name or not timezone:
        flash('All fields are required.', 'error')
        return redirect(url_for('main.profile'))

    # Validate timezone
    if timezone not in pytz.common_timezones:
        flash('Invalid timezone selected.', 'error')
        return redirect(url_for('main.profile'))

    # Update user
    current_user.update_profile(
        first_name=first_name,
        last_name=last_name,
        timezone=timezone
    )

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))


@main_bp.route('/profile/toggle-admin', methods=['POST'])
@login_required
def toggle_admin():
    """Toggle administrator status for the current user"""
    current_user.toggle_administrator()
    status = 'enabled' if current_user.is_administrator else 'disabled'
    flash(f'Administrator status {status}.', 'success')
    return redirect(url_for('main.profile'))