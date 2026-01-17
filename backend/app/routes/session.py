"""Logout route and token management."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.db.mongo import MongoDB
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('session', __name__, url_prefix='/api/session')


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user and invalidate token.
    
    Note: JWT tokens are stateless. This endpoint is mainly for
    frontend to signal logout. Token remains valid until expiry.
    For true token revocation, implement a token blacklist.
    """
    try:
        user_id = get_jwt_identity()
        logger.info(f"User {user_id} logged out")
        
        return jsonify({
            "success": True,
            "message": "Logged out successfully"
        }), 200
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({"success": False, "message": "Logout failed"}), 500


@bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """Refresh access token using current token.
    
    Returns new access token with extended expiry.
    """
    try:
        from flask_jwt_extended import create_access_token
        
        user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=user_id)
        
        logger.info(f"Token refreshed for user {user_id}")
        
        return jsonify({
            "success": True,
            "access_token": new_access_token,
            "message": "Token refreshed"
        }), 200
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return jsonify({"success": False, "message": "Token refresh failed"}), 500
