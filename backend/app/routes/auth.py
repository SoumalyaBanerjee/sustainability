"""Authentication routes."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.auth_service import AuthService
from app.models.user import User
from app.db.mongo import MongoDB
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """Register a new user.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        # Register user
        result = AuthService.register_user(email, password)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"success": False, "message": "Registration failed"}), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token.
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        # Authenticate user
        result = AuthService.login_user(email, password)
        
        if not result["success"]:
            return jsonify(result), 401
        
        # Create JWT token
        access_token = create_access_token(identity=result["user"]["id"])
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user": result["user"]
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"success": False, "message": "Login failed"}), 500


@bp.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    """Request password reset OTP.
    
    Request body:
    {
        "email": "user@example.com"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400
        
        # Request password reset
        result = AuthService.request_password_reset(email)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Password reset request error: {str(e)}")
        return jsonify({"success": False, "message": "Request failed"}), 500


@bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using OTP.
    
    Request body:
    {
        "email": "user@example.com",
        "otp": "123456",
        "new_password": "NewSecurePass123!"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        email = data.get('email', '').strip()
        otp = data.get('otp', '').strip()
        new_password = data.get('new_password', '')
        
        if not email or not otp or not new_password:
            return jsonify({"success": False, "message": "Email, OTP, and new password are required"}), 400
        
        # Reset password
        result = AuthService.verify_otp_and_reset_password(email, otp, new_password)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({"success": False, "message": "Password reset failed"}), 500


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info (requires JWT token)."""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "user": User.to_dict(user)
        }), 200
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({"success": False, "message": "Failed to get user info"}), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Test MongoDB connection
        MongoDB.get_db().command('ping')
        return jsonify({
            "status": "healthy",
            "service": "auth-service"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "service": "auth-service",
            "error": str(e)
        }), 503
