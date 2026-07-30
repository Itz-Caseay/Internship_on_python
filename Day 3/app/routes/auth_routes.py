from flask import Blueprint, request, jsonify
from ..controllers.auth_controller import AuthController
from ..middleware.auth_middleware import token_required

def create_auth_routes(auth_controller: AuthController):
    """Create auth routes blueprint"""
    auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
    
    # Public routes
    @auth_bp.route('/register', methods=['POST'])
    def register():
        return auth_controller.register()
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        return auth_controller.login()
    
    @auth_bp.route('/refresh-token', methods=['POST'])
    def refresh_token():
        return auth_controller.refresh_token()
    
    @auth_bp.route('/logout', methods=['POST'])
    def logout():
        return auth_controller.logout()
    
    # Protected routes
    @auth_bp.route('/profile', methods=['GET'])
    @token_required
    def get_profile():
        return auth_controller.get_profile(request.user['user_id'])
    
    @auth_bp.route('/profile', methods=['PUT'])
    @token_required
    def update_profile():
        return auth_controller.update_profile(request.user['user_id'])
    
    return auth_bp