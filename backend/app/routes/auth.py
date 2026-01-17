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


@bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify user email with token.
    
    Request body:
    {
        "token": "verification_token"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        token = data.get('token', '').strip()
        
        if not token:
            return jsonify({"success": False, "message": "Token is required"}), 400
        
        # Verify email
        result = AuthService.verify_email(token)
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Email verification error: {str(e)}")
        return jsonify({"success": False, "message": "Email verification failed"}), 500



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
        
        user = result["user"]
        
        # Check if email is verified
        if not user.get("is_verified"):
            return jsonify({
                "success": False,
                "message": "Please verify your email before logging in",
                "requires_email_verification": True,
                "email": email
            }), 403
        
        # Create JWT token
        access_token = create_access_token(identity=user["id"])
        
        # Check if 2FA is enabled
        if user.get("two_factor_enabled"):
            return jsonify({
                "success": True,
                "message": "2FA required",
                "access_token": access_token,
                "user": user,
                "requires_2fa": True
            }), 200
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user": user,
            "requires_2fa": False
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


@bp.route('/2fa/setup', methods=['POST'])
@jwt_required()
def setup_2fa():
    """Setup 2FA for user.
    
    Returns QR code URI and backup codes
    """
    try:
        from app.models.two_factor_auth import TwoFactorAuth
        
        user_id = get_jwt_identity()
        
        # Generate secret and backup codes
        secret, provisioning_uri = TwoFactorAuth.generate_secret()
        backup_codes = TwoFactorAuth.generate_backup_codes()
        
        # Store temporarily (user must verify with TOTP code before enabling)
        # For now, return to frontend
        
        return jsonify({
            "success": True,
            "secret": secret,
            "provisioning_uri": provisioning_uri,
            "backup_codes": backup_codes,
            "message": "Scan QR code with authenticator app and verify"
        }), 200
        
    except Exception as e:
        logger.error(f"2FA setup error: {str(e)}")
        return jsonify({"success": False, "message": "2FA setup failed"}), 500


@bp.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify_2fa_setup():
    """Verify and enable 2FA."""
    try:
        from app.models.two_factor_auth import TwoFactorAuth
        
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        secret = data.get('secret', '').strip()
        code = data.get('code', '').strip()
        backup_codes = data.get('backup_codes', [])
        
        if not secret or not code or not backup_codes:
            return jsonify({"success": False, "message": "Secret, code, and backup codes required"}), 400
        
        # Verify code
        import pyotp
        totp = pyotp.TOTP(secret)
        if not totp.verify(code, valid_window=1):
            return jsonify({"success": False, "message": "Invalid code"}), 400
        
        # Create 2FA record
        TwoFactorAuth.create_2fa(user_id, secret, backup_codes)
        
        # Enable 2FA
        TwoFactorAuth.enable_2fa(user_id)
        User.enable_2fa(user_id)
        
        return jsonify({
            "success": True,
            "message": "2FA enabled successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"2FA verification error: {str(e)}")
        return jsonify({"success": False, "message": "2FA verification failed"}), 500


@bp.route('/2fa/verify-code', methods=['POST'])
def verify_2fa_code():
    """Verify 2FA code during login."""
    try:
        from app.models.two_factor_auth import TwoFactorAuth
        
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        token = data.get('access_token', '').strip()
        code = data.get('code', '').strip()
        use_backup = data.get('use_backup', False)
        
        if not token or not code:
            return jsonify({"success": False, "message": "Token and code required"}), 400
        
        # Decode token to get user_id (without verification for temporary token)
        try:
            from flask_jwt_extended import decode_token
            decoded = decode_token(token)
            user_id = decoded.get('sub')
        except:
            return jsonify({"success": False, "message": "Invalid token"}), 401
        
        if use_backup:
            # Use backup code
            if TwoFactorAuth.use_backup_code(user_id, code):
                return jsonify({
                    "success": True,
                    "message": "2FA verified with backup code"
                }), 200
            else:
                return jsonify({"success": False, "message": "Invalid backup code"}), 400
        else:
            # Verify TOTP code
            if TwoFactorAuth.verify_totp(user_id, code):
                return jsonify({
                    "success": True,
                    "message": "2FA verified successfully"
                }), 200
            else:
                return jsonify({"success": False, "message": "Invalid 2FA code"}), 400
        
    except Exception as e:
        logger.error(f"2FA code verification error: {str(e)}")
        return jsonify({"success": False, "message": "2FA verification failed"}), 500


@bp.route('/2fa/disable', methods=['POST'])
@jwt_required()
def disable_2fa():
    """Disable 2FA for user."""
    try:
        from app.models.two_factor_auth import TwoFactorAuth
        
        user_id = get_jwt_identity()
        
        TwoFactorAuth.disable_2fa(user_id)
        User.disable_2fa(user_id)
        
        return jsonify({
            "success": True,
            "message": "2FA disabled successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"2FA disable error: {str(e)}")
        return jsonify({"success": False, "message": "2FA disable failed"}), 500
