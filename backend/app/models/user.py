"""User model for MongoDB."""

from datetime import datetime
from bson.objectid import ObjectId
from app.db.mongo import MongoDB


class User:
    """User model."""
    
    COLLECTION_NAME = "users"
    
    @classmethod
    def get_collection(cls):
        """Get users collection."""
        return MongoDB.get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    def create_indexes(cls):
        """Create indexes for users collection."""
        collection = cls.get_collection()
        collection.create_index("email", unique=True)
        collection.create_index("created_at")
    
    @classmethod
    def create_user(cls, email, hashed_password, is_verified=True):
        """Create a new user."""
        collection = cls.get_collection()
        user_data = {
            "email": email,
            "password": hashed_password,
            "is_active": True,
            "is_verified": is_verified,
            "two_factor_enabled": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = collection.insert_one(user_data)
        return str(result.inserted_id)
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        collection = cls.get_collection()
        return collection.find_one({"email": email})
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        collection = cls.get_collection()
        try:
            return collection.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
    
    @classmethod
    def update_password(cls, user_id, hashed_password):
        """Update user password."""
        collection = cls.get_collection()
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "password": hashed_password,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @classmethod
    def to_dict(cls, user_doc):
        """Convert user document to dictionary."""
        if user_doc is None:
            return None
        return {
            "id": str(user_doc["_id"]),
            "email": user_doc["email"],
            "is_active": user_doc.get("is_active", True),
            "is_verified": user_doc.get("is_verified", True),
            "two_factor_enabled": user_doc.get("two_factor_enabled", False),
            "created_at": user_doc.get("created_at"),
            "updated_at": user_doc.get("updated_at")
        }
    
    @classmethod
    def mark_verified(cls, user_id):
        """Mark user email as verified."""
        collection = cls.get_collection()
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_verified": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @classmethod
    def enable_2fa(cls, user_id):
        """Enable 2FA for user."""
        collection = cls.get_collection()
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "two_factor_enabled": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @classmethod
    def disable_2fa(cls, user_id):
        """Disable 2FA for user."""
        collection = cls.get_collection()
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "two_factor_enabled": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
