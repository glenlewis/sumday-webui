from datetime import datetime
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    timezone = db.Column(db.String(50), nullable=False, default='UTC')
    is_administrator = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    @property
    def full_name(self):
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"

    def update_profile(self, first_name=None, last_name=None, timezone=None):
        """Update user profile information"""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if timezone:
            self.timezone = timezone
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def toggle_administrator(self):
        """Toggle administrator status"""
        self.is_administrator = not self.is_administrator
        self.updated_at = datetime.utcnow()
        db.session.commit()