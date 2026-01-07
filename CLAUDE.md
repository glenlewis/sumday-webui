# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sumday is a Flask-based web application with Auth0 authentication and PostgreSQL database support. Users can create accounts, authenticate via Auth0, and manage their profile information including name and timezone preferences.

## Development Commands

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Auth0 and database credentials
```

### Database Setup
```bash
# Create PostgreSQL database (using the name from your .env)
createdb sumday

# Run database migrations
flask db upgrade

# To create a new migration after model changes
flask db migrate -m "Description of changes"
flask db upgrade
```

### Running the Application
```bash
# Development server
python run.py

# Or using Flask CLI
export FLASK_APP=run.py
flask run
```

## Architecture

### Project Structure
- `app/` - Main application package
  - `auth/` - Authentication routes and Auth0 integration
  - `main/` - Main application routes (home, profile)
  - `templates/` - Jinja2 HTML templates
  - `static/` - CSS, JavaScript, and static assets
  - `models.py` - SQLAlchemy database models
- `config.py` - Application configuration
- `run.py` - Application entry point

### Database Models
- `User` - Stores user profile information
  - `auth0_id` - Auth0 unique identifier
  - `email` - User email address
  - `first_name`, `last_name` - User's name
  - `timezone` - User's preferred timezone
  - `is_administrator` - Administrator flag (boolean, default: False)
  - `created_at`, `updated_at` - Timestamps

### Authentication Flow
1. User clicks login → redirects to Auth0
2. Auth0 authenticates user → redirects to `/callback`
3. If new user → redirects to `/register` to complete profile
4. If existing user → logs in and redirects to `/profile`

### Key Dependencies
- Flask - Web framework
- Flask-SQLAlchemy - ORM for database
- Flask-Migrate - Database migrations (Alembic)
- Flask-Login - User session management
- Authlib - Auth0 OAuth integration
- psycopg2-binary - PostgreSQL adapter
- pytz - Timezone support

### Database Migrations
This project uses Flask-Migrate (Alembic) for database schema management.

#### Common Migration Commands
```bash
# Create a new migration after changing models
flask db migrate -m "Description of your changes"

# Apply migrations to database
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history

# View current database version
flask db current
```