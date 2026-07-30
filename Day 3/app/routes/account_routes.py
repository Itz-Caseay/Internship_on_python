from flask import Blueprint, request, jsonify
from ..controllers.account_controller import AccountController
from ..middleware.auth_middleware import token_required

def create_account_routes(account_controller: AccountController):
    """Create account routes blueprint"""
    account_bp = Blueprint('accounts', __name__, url_prefix='/api')
    
    # All routes require authentication
    @account_bp.route('/accounts', methods=['POST'])
    @token_required
    def create_account():
        return account_controller.create_account(request.user['user_id'])
    
    @account_bp.route('/accounts', methods=['GET'])
    @token_required
    def get_accounts():
        return account_controller.get_accounts(request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>', methods=['GET'])
    @token_required
    def get_account(account_id):
        return account_controller.get_account(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/balance', methods=['GET'])
    @token_required
    def get_balance(account_id):
        return account_controller.get_balance(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/deposit', methods=['POST'])
    @token_required
    def deposit(account_id):
        return account_controller.deposit(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/withdraw', methods=['POST'])
    @token_required
    def withdraw(account_id):
        return account_controller.withdraw(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/transfer', methods=['POST'])
    @token_required
    def transfer(account_id):
        return account_controller.transfer(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/transactions', methods=['GET'])
    @token_required
    def get_transactions(account_id):
        return account_controller.get_transactions(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/freeze', methods=['POST'])
    @token_required
    def freeze_account(account_id):
        return account_controller.freeze_account(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>/unfreeze', methods=['POST'])
    @token_required
    def unfreeze_account(account_id):
        return account_controller.unfreeze_account(account_id, request.user['user_id'])
    
    @account_bp.route('/accounts/<account_id>', methods=['DELETE'])
    @token_required
    def close_account(account_id):
        return account_controller.close_account(account_id, request.user['user_id'])
    
    return account_bp