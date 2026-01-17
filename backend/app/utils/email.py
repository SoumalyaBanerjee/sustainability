"""Email utilities for sending OTP and verification emails."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import logging

logger = logging.getLogger(__name__)


def send_otp_email(recipient_email: str, otp_code: str) -> bool:
    """Send OTP to email address.
    
    Args:
        recipient_email: Email address to send OTP to
        otp_code: OTP code to send
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        smtp_server = current_app.config['SMTP_SERVER']
        smtp_port = current_app.config['SMTP_PORT']
        sender_email = current_app.config['SMTP_EMAIL']
        sender_password = current_app.config['SMTP_PASSWORD']
        sender_name = current_app.config['SMTP_FROM_NAME']
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset OTP"
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = recipient_email
        
        # Create email body
        text = f"""
Hello,

Your password reset OTP is: {otp_code}

This OTP will expire in 10 minutes.

If you did not request a password reset, please ignore this email.

Best regards,
{sender_name}
        """
        
        html = f"""\
<html>
  <body>
    <p>Hello,</p>
    <p>Your password reset OTP is: <strong>{otp_code}</strong></p>
    <p>This OTP will expire in 10 minutes.</p>
    <p>If you did not request a password reset, please ignore this email.</p>
    <p>Best regards,<br>{sender_name}</p>
  </body>
</html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        logger.info(f"OTP email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
        return False


def send_verification_email(recipient_email: str, verification_token: str) -> bool:
    """Send email verification link.
    
    Args:
        recipient_email: Email address to verify
        verification_token: Verification token
        
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        smtp_server = current_app.config['SMTP_SERVER']
        smtp_port = current_app.config['SMTP_PORT']
        sender_email = current_app.config['SMTP_EMAIL']
        sender_password = current_app.config['SMTP_PASSWORD']
        sender_name = current_app.config['SMTP_FROM_NAME']
        
        # Verification link (update with your frontend URL)
        verification_link = f"http://localhost:8000/verify-email?token={verification_token}"
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Email Verification Required"
        message["From"] = f"{sender_name} <{sender_email}>"
        message["To"] = recipient_email
        
        # Create email body
        text = f"""
Hello,

Thank you for registering with {sender_name}!

Please verify your email by clicking the link below:
{verification_link}

This link will expire in 24 hours.

If you did not create this account, please ignore this email.

Best regards,
{sender_name}
        """
        
        html = f"""\
<html>
  <body>
    <p>Hello,</p>
    <p>Thank you for registering with {sender_name}!</p>
    <p>Please verify your email by clicking the link below:</p>
    <p><a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
    <p>This link will expire in 24 hours.</p>
    <p>If you did not create this account, please ignore this email.</p>
    <p>Best regards,<br>{sender_name}</p>
  </body>
</html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        logger.info(f"Verification email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        return False
