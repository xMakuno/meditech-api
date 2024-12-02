from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vamos-a-china2025!@localhost:5432/postgres'

    db.init_app(app)

    # Import and register all blueprints

    from .appointments.routes import appointments
    from .auth.routes import auth

    app.register_blueprint(appointments, url_prefix='/appointments')
    app.register_blueprint(auth, url_prefix='/auth')
    migrate = Migrate(app, db)

    return app