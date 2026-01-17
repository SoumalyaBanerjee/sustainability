"""Two-Factor Authentication model for MongoDB."""

from datetime import datetime
from app.db.mongo import MongoDB
import pyotp
import secrets


class TwoFactorAuth:
    """2FA settings and backup codes for users."""
    
    COLLECTION_NAME = "two_factor_auth"
    
    @classmethod
    def get_collection(cls):
        """Get 2FA collection."""
        return MongoDB.get_collection(cls.COLLECTION_NAME)
    
    @classmethod
    def create_indexes(cls):
        """Create indexes for 2FA collection."""
        collection = cls.get_collection()
        collection.create_index("user_id", unique=True)
    
    @classmethod
    def generate_secret(cls):
        """Generate TOTP secret for 2FA.
        
        Returns:
            Tuple of (secret, provisioning_uri)
        """
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name="Sustainability",
            issuer_name="Sustainability App"
        )
        return secret, provisioning_uri
    
    @classmethod
    def generate_backup_codes(cls, count=10):
        """Generate backup codes for account recovery.
        
        Args:
            count: Number of backup codes to generate
            
        Returns:
            List of backup codes
        """
        return [secrets.token_hex(4) for _ in range(count)]
    
    @classmethod
    def create_2fa(cls, user_id, secret, backup_codes):
        """Create 2FA record for user.
        
        Args:
            user_id: User ID
            secret: TOTP secret
            backup_codes: List of backup codes
        """
        collection = cls.get_collection()
        
        twofa_data = {
            "user_id": user_id,
            "secret": secret,
            "is_enabled": False,
            "backup_codes": backup_codes,
            "used_backup_codes": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = collection.insert_one(twofa_data)
        return str(result.inserted_id)
    
    @classmethod
    def find_by_user(cls, user_id):
        """Find 2FA settings by user ID."""
        collection = cls.get_collection()
        from bson.objectid import ObjectId
        try:
            return collection.find_one({"user_id": ObjectId(user_id)})
        except:
            return None
    
    @classmethod
    def enable_2fa(cls, user_id):
        """Enable 2FA for user."""
        collection = cls.get_collection()
        from bson.objectid import ObjectId
        result = collection.update_one(
            {"user_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_enabled": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    @classmethod
    def verify_totp(cls, user_id, code):
        """Verify TOTP code."""
        twofa = cls.find_by_user(user_id)
        if not twofa or not twofa.get("is_enabled"):
            return False
        
        secret = twofa.get("secret")
        totp = pyotp.TOTP(secret)
        
        # Allow 1 time step tolerance (30 seconds)
        return totp.verify(code, valid_window=1)
    
    @classmethod
    def use_backup_code(cls, user_id, code):
        """Use a backup code."""
        collection = cls.get_collection()
        from bson.objectid import ObjectId
        
        twofa = cls.find_by_user(user_id)
        if not twofa or code not in twofa.get("backup_codes", []):
            return False
        
        if code in twofa.get("used_backup_codes", []):
            return False
        
        # Mark as used
        result = collection.update_one(
            {"user_id": ObjectId(user_id)},
            {
                "$push": {"used_backup_codes": code},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0
    
    @classmethod
    def disable_2fa(cls, user_id):
        """Disable 2FA for user."""
        collection = cls.get_collection()
        from bson.objectid import ObjectId
        result = collection.update_one(
            {"user_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_enabled": False,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
