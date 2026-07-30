from flask import request, jsonify
from ..services.auth_service import AuthService

class AuthController:
    """Controller for authentication endpoints"""
    
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
    
    def register(self):
        """Register a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'full_name']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'Missing required field: {field}'
                    }), 400
            
            user = self.auth_service.register(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                full_name=data['full_name']
            )
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': user.to_dict()
            }), 201
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Registration failed'
            }), 500
    
    def login(self):
        """Login user"""
        try:
            data = request.get_json()
            
            if not data.get('username') or not data.get('password'):
                return jsonify({
                    'success': False,
                    'message': 'Username and password required'
                }), 400
            
            user, access_token, refresh_token = self.auth_service.login(
                username=data['username'],
                password=data['password']
            )
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user': user.to_dict(),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Login failed'
            }), 500
    
    def refresh_token(self):
        """Refresh access token"""
        try:
            data = request.get_json()
            refresh_token = data.get('refresh_token')
            
            if not refresh_token:
                return jsonify({
                    'success': False,
                    'message': 'Refresh token required'
                }), 400
            
            new_access_token = self.auth_service.refresh_access_token(refresh_token)
            
            return jsonify({
                'success': True,
                'data': {
                    'access_token': new_access_token
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Token refresh failed'
            }), 500
    
    def logout(self):
        """Logout user"""
        try:
            data = request.get_json()
            refresh_token = data.get('refresh_token')
            
            if refresh_token:
                self.auth_service.logout(refresh_token)
            
            return jsonify({
                'success': True,
                'message': 'Logout successful'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Logout failed'
            }), 500
    
    def get_profile(self, user_id):
        """Get current user profile"""
        try:
            user = self.auth_service.get_user(user_id)
            
            return jsonify({
                'success': True,
                'data': user.to_dict()
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to get profile'
            }), 500
    
    def update_profile(self, user_id):
        """Update user profile"""
        try:
            data = request.get_json()
            
            user = self.auth_service.update_user(
                user_id=user_id,
                full_name=data.get('full_name'),
                email=data.get('email')
            )
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'data': user.to_dict()
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to update profile'
            }), 500