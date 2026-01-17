"""Authentication service for user management."""

from app.models.user import User
from app.models.otp import OTP
from app.models.email_verification import EmailVerification
from app.models.two_factor_auth import TwoFactorAuth
from app.utils.password import hash_password, verify_password
from app.utils.email import send_otp_email, send_verification_email
from app.utils.otp_generator import generate_otp
from app.utils.validators import validate_email_format, validate_password, validate_otp


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(email: str, password: str) -> dict:
        """Register a new user.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Result dictionary with status and message
        """
        # Validate email format
        is_valid_email, message = validate_email_format(email)
        if not is_valid_email:
            return {"success": False, "message": f"Invalid email: {message}"}
        
        # Validate password strength
        is_valid_password, message = validate_password(password)
        if not is_valid_password:
            return {"success": False, "message": message}
        
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return {"success": False, "message": "User already exists"}
        
        # Hash password and create user (not verified yet)
        hashed_password = hash_password(password)
        user_id = User.create_user(email, hashed_password, is_verified=False)
        
        # Generate email verification token
        verification_token = EmailVerification.create_verification(email)
        
        # Send verification email
        email_sent = send_verification_email(email, verification_token)
        
        if not email_sent:
            return {
                "success": True,
                "message": "User registered. Please check your email to verify (email system may be down)",
                "user_id": user_id,
                "email": email
            }
        
        return {
            "success": True,
            "message": "User registered successfully. Please verify your email.",
            "user_id": user_id,
            "email": email
        }
    
    @staticmethod
    def verify_email(token: str) -> dict:
        """Verify user email with token.
        
        Args:
            token: Verification token
            
        Returns:
            Result dictionary with status
        """
        # Find verification record
        verification = EmailVerification.find_by_token(token)
        if not verification:
            return {"success": False, "message": "Invalid or expired verification token"}
        
        email = verification.get("email")
        user = User.find_by_email(email)
        
        if not user:
            return {"success": False, "message": "User not found"}
        
        # Mark email as verified
        User.mark_verified(str(user["_id"]))
        EmailVerification.mark_verified(token)
        
        return {"success": True, "message": "Email verified successfully"}
    
    
    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """Authenticate user login.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Result dictionary with status and user info
        """
        # Find user by email
        user = User.find_by_email(email)
        if not user:
            return {"success": False, "message": "Invalid email or password"}
        
        # Verify password
        if not verify_password(password, user["password"]):
            return {"success": False, "message": "Invalid email or password"}
        
        # Check if user is active
        if not user.get("is_active", True):
            return {"success": False, "message": "User account is inactive"}
        
        return {
            "success": True,
            "message": "Login successful",
            "user": User.to_dict(user)
        }
    
    @staticmethod
    def request_password_reset(email: str) -> dict:
        """Request password reset by sending OTP.
        
        Args:
            email: User email
            
        Returns:
            Result dictionary with status
        """
        # Check if user exists
        user = User.find_by_email(email)
        if not user:
            # Don't reveal if user exists or not for security
            return {
                "success": True,
                "message": "If the email exists, an OTP will be sent"
            }
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Save OTP to database
        OTP.create_otp(email, otp_code)
        
        # Send OTP via email
        email_sent = send_otp_email(email, otp_code)
        
        if not email_sent:
            return {
                "success": False,
                "message": "Failed to send OTP email"
            }
        
        return {
            "success": True,
            "message": "OTP sent to your email"
        }
    
    @staticmethod
    def verify_otp_and_reset_password(email: str, otp: str, new_password: str) -> dict:
        """Verify OTP and reset password.
        
        Args:
            email: User email
            otp: OTP code
            new_password: New password
            
        Returns:
            Result dictionary with status
        """
        # Validate OTP format
        is_valid_otp, message = validate_otp(otp)
        if not is_valid_otp:
            return {"success": False, "message": message}
        
        # Validate password strength
        is_valid_password, message = validate_password(new_password)
        if not is_valid_password:
            return {"success": False, "message": message}
        
        # Find and verify OTP
        otp_record = OTP.find_valid_otp(email, otp)
        if not otp_record:
            return {"success": False, "message": "Invalid or expired OTP"}
        
        # Find user and update password
        user = User.find_by_email(email)
        if not user:
            return {"success": False, "message": "User not found"}
        
        # Hash new password and update
        hashed_password = hash_password(new_password)
        success = User.update_password(str(user["_id"]), hashed_password)
        
        if success:
            # Mark OTP as used
            OTP.mark_as_used(str(otp_record["_id"]))
            return {
                "success": True,
                "message": "Password reset successfully"
            }
        
        return {
            "success": False,
            "message": "Failed to reset password"
        }
