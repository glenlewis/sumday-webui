import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Make database available in Flask shell"""
    return {'db': db}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)