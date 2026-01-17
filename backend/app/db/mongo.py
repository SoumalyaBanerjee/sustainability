"""MongoDB connection and management."""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from flask import current_app
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB connection manager."""
    
    _instance = None
    _client = None
    _db = None
    
    def __init__(self):
        """Initialize MongoDB connection."""
        if MongoDB._client is None:
            try:
                MongoDB._client = MongoClient(
                    current_app.config['MONGODB_URI'],
                    serverSelectionTimeoutMS=5000
                )
                # Test connection
                MongoDB._client.admin.command('ping')
                MongoDB._db = MongoDB._client[current_app.config['MONGODB_DB_NAME']]
                logger.info("Connected to MongoDB")
            except ServerSelectionTimeoutError:
                logger.error("Failed to connect to MongoDB")
                raise
    
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if cls._db is None:
            cls()
        return cls._db
    
    @classmethod
    def get_collection(cls, collection_name):
        """Get specific collection."""
        db = cls.get_db()
        return db[collection_name]
    
    @classmethod
    def close(cls):
        """Close database connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("Disconnected from MongoDB")


def get_mongo():
    """Get MongoDB instance."""
    return MongoDB()
