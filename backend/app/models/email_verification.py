"""Email Verification model for MongoDB."""

from datetime import datetime, timedelta
from flask import current_app
from app.db.mongo import MongoDB
import secrets


class EmailVerification:
    """Email verification tokens for new registrations."""
    
    COLLECTION_NAME = "email_verifications"
    TOKEN_LENGTH = 32
    
    @classmethod
    def get_collection(cls):
        """Get email verification collection."""
        return MongoDB.get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    def create_indexes(cls):
        """Create indexes for email verification collection."""
        collection = cls.get_collection()
        collection.create_index("email", unique=False)
        collection.create_index("expires_at", expireAfterSeconds=0)
    
    @classmethod
    def create_verification(cls, email):
        """Create email verification token.
        
        Args:
            email: Email address to verify
            
        Returns:
            Verification token string
        """
        collection = cls.get_collection()
        
        # Generate secure token
        token = secrets.token_urlsafe(cls.TOKEN_LENGTH)
        
        verification_data = {
            "email": email,
            "token": token,
            "is_verified": False,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=24)
        }
        
        result = collection.insert_one(verification_data)
        return token
    
    @classmethod
    def find_by_token(cls, token):
        """Find verification record by token."""
        collection = cls.get_collection()
        return collection.find_one({
            "token": token,
            "is_verified": False,
            "expires_at": {"$gt": datetime.utcnow()}
        })
    
    @classmethod
    def mark_verified(cls, token):
        """Mark email as verified."""
        collection = cls.get_collection()
        result = collection.update_one(
            {"token": token},
            {"$set": {"is_verified": True}}
        )
        return result.modified_count > 0
    
    @classmethod
    def get_email_by_token(cls, token):
        """Get email from verification token."""
        record = cls.find_by_token(token)
        if record:
            return record.get("email")
        return None
