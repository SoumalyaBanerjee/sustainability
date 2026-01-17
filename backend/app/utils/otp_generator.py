"""OTP generation utility."""

import random


def generate_otp(length: int = 6) -> str:
    """Generate a random OTP.
    
    Args:
        length: Length of OTP (default 6)
        
    Returns:
        OTP string
    """
    return ''.join(str(random.randint(0, 9)) for _ in range(length))
