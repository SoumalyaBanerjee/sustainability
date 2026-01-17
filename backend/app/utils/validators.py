"""Input validation utilities."""

from email_validator import validate_email, EmailNotValidError
import re


def validate_email_format(email: str) -> tuple[bool, str]:
    """Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"


def validate_otp(otp: str) -> tuple[bool, str]:
    """Validate OTP format.
    
    Args:
        otp: OTP to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not otp or len(otp) != 6 or not otp.isdigit():
        return False, "OTP must be 6 digits"
    
    return True, "OTP is valid"
