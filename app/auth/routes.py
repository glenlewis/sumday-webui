from flask import redirect, url_for, session, request, flash, render_template, current_app
from flask_login import login_user, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode
from app.auth import auth_bp
from app import db, login_manager
from app.models import User
import pytz

oauth = OAuth()


def init_oauth(app):
    """Initialize OAuth with the app"""
    oauth.init_app(app)
    oauth.register(
        'auth0',
        client_id=app.config['AUTH0_CLIENT_ID'],
        client_secret=app.config['AUTH0_CLIENT_SECRET'],
        server_metadata_url=f"https://{app.config['AUTH0_DOMAIN']}/.well-known/openid-configuration",
        client_kwargs={
            'scope': 'openid profile email',
        },
    )


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@auth_bp.before_app_request
def initialize_oauth():
    """Initialize OAuth before first request"""
    if not hasattr(auth_bp, 'oauth_initialized'):
        init_oauth(current_app)
        auth_bp.oauth_initialized = True


@auth_bp.route('/login')
def login():
    """Redirect to Auth0 login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri)


@auth_bp.route('/callback')
def callback():
    """Handle Auth0 callback"""
    token = oauth.auth0.authorize_access_token()

    # Get user info from the token (ID token contains user claims)
    userinfo = token.get('userinfo')

    # Check if user exists in database
    user = User.query.filter_by(auth0_id=userinfo['sub']).first()

    if not user:
        # New user - redirect to registration form with Auth0 data
        session['auth0_userinfo'] = userinfo
        return redirect(url_for('auth.register'))

    # Check if user is active
    if not user.is_active:
        flash('Your account has been deactivated. Please contact an administrator.', 'error')
        return redirect(url_for('main.index'))

    # Existing user - log them in
    login_user(user)
    return redirect(url_for('main.profile'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    # Check if we have Auth0 user info in session
    userinfo = session.get('auth0_userinfo')
    if not userinfo:
        flash('Please log in with Auth0 first.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        timezone = request.form.get('timezone', 'UTC')

        # Create new user
        user = User(
            auth0_id=userinfo['sub'],
            email=userinfo['email'],
            first_name=first_name,
            last_name=last_name,
            timezone=timezone
        )

        db.session.add(user)
        db.session.commit()

        # Clear session data
        session.pop('auth0_userinfo', None)

        # Log user in
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.profile'))

    # GET request - show registration form
    timezones = pytz.common_timezones
    return render_template('auth/register.html', userinfo=userinfo, timezones=timezones)


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    session.clear()

    # Redirect to Auth0 logout
    params = {
        'returnTo': url_for('main.index', _external=True),
        'client_id': current_app.config['AUTH0_CLIENT_ID']
    }

    return redirect(f"https://{current_app.config['AUTH0_DOMAIN']}/v2/logout?{urlencode(params)}")