"""Run Flask application."""

import os
import logging
from app import create_app
from app.models.user import User
from app.models.otp import OTP
from app.models.email_verification import EmailVerification
from app.models.two_factor_auth import TwoFactorAuth
from app.db.mongo import MongoDB

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize database indexes."""
    try:
        User.create_indexes()
        OTP.create_indexes()
        EmailVerification.create_indexes()
        TwoFactorAuth.create_indexes()
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Failed to create indexes: {str(e)}")


if __name__ == '__main__':
    app = create_app()
    
    # Initialize database on startup
    with app.app_context():
        init_db()
    
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
