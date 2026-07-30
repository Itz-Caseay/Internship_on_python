from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Configure app
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET', '5ca04f9d68b7e1f91d368185d76d6c25fc548da761b29507fb03fae622971e64')
    app.config['JWT_REFRESH_SECRET'] = os.getenv('JWT_REFRESH_SECRET', '0a7955265abc373d2a40cab9cad88c8c65050ea0cb7f48f5a3b7f4cd4147077b')
    
    # Initialize services
    from .services.auth_service import AuthService
    from .services.banking_service import BankingService
    from .controllers.auth_controller import AuthController
    from .controllers.account_controller import AccountController
    from .routes.auth_routes import create_auth_routes
    from .routes.account_routes import create_account_routes
    
    auth_service = AuthService()
    banking_service = BankingService()
    
    auth_controller = AuthController(auth_service)
    account_controller = AccountController(banking_service)
    
    # Register blueprints
    app.register_blueprint(create_auth_routes(auth_controller))
    app.register_blueprint(create_account_routes(account_controller))
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'OK',
            'timestamp': datetime.now().isoformat(),
            'uptime': 'Running'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Route not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    return app