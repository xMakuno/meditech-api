import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session  # Flask-Session for session management
from flask_login import LoginManager  # Flask-Login for user authentication
from flask_cors import CORS
# Initialize the database instance
db = SQLAlchemy()

# Initialize the login manager
login_manager = LoginManager()

# Location for files
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

def create_app():
    app = Flask(__name__)
    # Enable CORS for all routes and origins
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # Configure the app (consider moving sensitive keys to environment variables)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vamos-a-china2025!@localhost:5432/postgres'
    app.config['SECRET_KEY'] = 'meditech-secret'  # Set a secure key for signing cookies and sessions
    
    # Flask-Session Configuration
    app.config['SESSION_TYPE'] = 'filesystem'  # Or 'redis' for production
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies to prevent tampering

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # Initialize Flask extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    Session(app)  # Flask-Session for server-side sessions
    login_manager.init_app(app)  # Flask-Login for managing user sessions

    # Register Blueprints
    from .appointments.routes import appointments
    from .auth.routes import auth
    from .doctors.routes import doctors
    from .hospitals.routes import hospitals
    from .insurances.routes import insurances
    from .subscriptions.routes import subscriptions
    from .medications.routes import medications
    from .examinations.routes import examinations
    from .users.routes import users

    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(doctors, url_prefix='/doctors')
    app.register_blueprint(hospitals, url_prefix='/hospitals')
    app.register_blueprint(insurances, url_prefix='/insurances')
    app.register_blueprint(subscriptions, url_prefix='/subscriptions')
    app.register_blueprint(medications, url_prefix='/medications')
    app.register_blueprint(examinations, url_prefix='/examinations')
    app.register_blueprint(users, url_prefix='/users')

    # Setup login manager (user loader function)
    @login_manager.user_loader
    def load_user(user_id):
        from .users.models import User
        return User.query.get(user_id)

    return app