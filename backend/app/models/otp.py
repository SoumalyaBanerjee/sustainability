"""OTP model for MongoDB."""

from datetime import datetime, timedelta
from flask import current_app
from app.db.mongo import MongoDB


class OTP:
    """OTP model for password reset."""
    
    COLLECTION_NAME = "otps"
    
    @classmethod
    def get_collection(cls):
        """Get OTP collection."""
        return MongoDB.get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    def create_indexes(cls):
        """Create indexes for OTP collection."""
        collection = cls.get_collection()
        collection.create_index("email", unique=False)
        collection.create_index("expires_at", expireAfterSeconds=0)
    
    @classmethod
    def create_otp(cls, email, otp_code):
        """Create OTP for email."""
        collection = cls.get_collection()
        expiry_minutes = current_app.config['OTP_EXPIRY_MINUTES']
        
        otp_data = {
            "email": email,
            "code": otp_code,
            "is_used": False,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(minutes=expiry_minutes)
        }
        result = collection.insert_one(otp_data)
        return str(result.inserted_id)
    
    @classmethod
    def find_valid_otp(cls, email, otp_code):
        """Find valid OTP for email."""
        collection = cls.get_collection()
        return collection.find_one({
            "email": email,
            "code": otp_code,
            "is_used": False,
            "expires_at": {"$gt": datetime.utcnow()}
        })
    
    @classmethod
    def mark_as_used(cls, otp_id):
        """Mark OTP as used."""
        from bson.objectid import ObjectId
        collection = cls.get_collection()
        result = collection.update_one(
            {"_id": ObjectId(otp_id)},
            {"$set": {"is_used": True}}
        )
        return result.modified_count > 0
    
    @classmethod
    def delete_used_otps(cls, email):
        """Delete all used OTPs for email."""
        collection = cls.get_collection()
        collection.delete_many({
            "email": email,
            "is_used": True
        })
