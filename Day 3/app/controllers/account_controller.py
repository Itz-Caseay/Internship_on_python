from flask import request, jsonify
from ..services.banking_service import BankingService

class AccountController:
    """Controller for account endpoints"""
    
    def __init__(self, banking_service: BankingService):
        self.banking_service = banking_service
    
    def create_account(self, user_id):
        """Create a new account"""
        try:
            data = request.get_json()
            
            account_type = data.get('account_type', 'savings')
            initial_deposit = data.get('initial_deposit', 0.0)
            
            # Get user from auth service (should be passed in)
            # For now, we'll assume user_id is valid
            from ..services.auth_service import AuthService
            auth_service = AuthService()
            user = auth_service.get_user(user_id)
            
            account = self.banking_service.create_account(user, account_type, initial_deposit)
            
            return jsonify({
                'success': True,
                'message': 'Account created successfully',
                'data': account.get_summary()
            }), 201
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to create account'
            }), 500
    
    def get_accounts(self, user_id):
        """Get all accounts for a user"""
        try:
            accounts = self.banking_service.get_user_accounts(user_id)
            
            return jsonify({
                'success': True,
                'data': [account.get_summary() for account in accounts]
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to get accounts'
            }), 500
    
    def get_account(self, account_id, user_id):
        """Get account details"""
        try:
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            return jsonify({
                'success': True,
                'data': account.get_summary()
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to get account'
            }), 500
    
    def get_balance(self, account_id, user_id):
        """Get account balance"""
        try:
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            return jsonify({
                'success': True,
                'data': {
                    'account_number': account.account_number,
                    'balance': account.balance,
                    'currency': account.currency
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to get balance'
            }), 500
    
    def deposit(self, account_id, user_id):
        """Deposit money"""
        try:
            data = request.get_json()
            amount = data.get('amount')
            description = data.get('description', 'Deposit')
            
            if not amount or amount <= 0:
                return jsonify({
                    'success': False,
                    'message': 'Valid amount required'
                }), 400
            
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            transaction = self.banking_service.deposit(account_id, float(amount), description)
            
            return jsonify({
                'success': True,
                'message': 'Deposit successful',
                'data': {
                    'transaction': transaction,
                    'balance': account.balance
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to process deposit'
            }), 500
    
    def withdraw(self, account_id, user_id):
        """Withdraw money"""
        try:
            data = request.get_json()
            amount = data.get('amount')
            description = data.get('description', 'Withdrawal')
            
            if not amount or amount <= 0:
                return jsonify({
                    'success': False,
                    'message': 'Valid amount required'
                }), 400
            
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            transaction = self.banking_service.withdraw(account_id, float(amount), description)
            
            return jsonify({
                'success': True,
                'message': 'Withdrawal successful',
                'data': {
                    'transaction': transaction,
                    'balance': account.balance
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to process withdrawal'
            }), 500
    
    def transfer(self, account_id, user_id):
        """Transfer money"""
        try:
            data = request.get_json()
            to_account_number = data.get('to_account_number')
            amount = data.get('amount')
            description = data.get('description', 'Transfer')
            
            if not amount or amount <= 0:
                return jsonify({
                    'success': False,
                    'message': 'Valid amount required'
                }), 400
            
            if not to_account_number:
                return jsonify({
                    'success': False,
                    'message': 'Destination account required'
                }), 400
            
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            transfer_result = self.banking_service.transfer(
                account_id,
                to_account_number,
                float(amount),
                description
            )
            
            return jsonify({
                'success': True,
                'message': 'Transfer successful',
                'data': transfer_result
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to process transfer'
            }), 500
    
    def get_transactions(self, account_id, user_id):
        """Get transaction history"""
        try:
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            transactions = self.banking_service.get_transaction_history(account_id, limit, offset)
            
            return jsonify({
                'success': True,
                'data': {
                    'transactions': transactions,
                    'total': len(account.transactions),
                    'limit': limit,
                    'offset': offset
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to get transactions'
            }), 500
    
    def freeze_account(self, account_id, user_id):
        """Freeze account"""
        try:
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            self.banking_service.freeze_account(account_id)
            
            return jsonify({
                'success': True,
                'message': 'Account frozen successfully',
                'data': account.get_summary()
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to freeze account'
            }), 500
    
    def unfreeze_account(self, account_id, user_id):
        """Unfreeze account"""
        try:
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            self.banking_service.unfreeze_account(account_id)
            
            return jsonify({
                'success': True,
                'message': 'Account unfrozen successfully',
                'data': account.get_summary()
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to unfreeze account'
            }), 500
    
    def close_account(self, account_id, user_id):
        """Close account"""
        try:
            account = self.banking_service.get_account(account_id)
            
            # Verify ownership
            if account.user_id != user_id:
                return jsonify({
                    'success': False,
                    'message': 'Access denied'
                }), 403
            
            self.banking_service.close_account(account_id)
            
            return jsonify({
                'success': True,
                'message': 'Account closed successfully'
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Failed to close account'
            }), 500