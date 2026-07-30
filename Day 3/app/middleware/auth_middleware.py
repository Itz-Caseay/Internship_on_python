from functools import wraps
from flask import request, jsonify, current_app
import jwt
import os

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'No token provided'
            }), 401
        
        try:
            # Verify token
            jwt_secret = os.getenv('JWT_SECRET', '5ca04f9d68b7e1f91d368185d76d6c25fc548da761b29507fb03fae622971e64')
            payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            
            # Add user info to request
            request.user = {
                'user_id': payload['user_id'],
                'username': payload['username'],
                'email': payload['email']
            }
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated

def get_current_user(auth_service, user_id):
    """Helper to get current user from auth service"""
    try:
        return auth_service.get_user(user_id)
    except ValueError:
        return None