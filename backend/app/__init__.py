"""Initialize Flask application."""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize JWT
    JWTManager(app)
    
    # Register blueprints
    from app.routes import auth, user, session, audits
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(session.bp)
    app.register_blueprint(audits.bp)
    
    return app
