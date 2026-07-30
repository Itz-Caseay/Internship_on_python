from typing import List, Dict, Optional
from ..models.account import Account
from ..models.transaction import Transaction

class BankingService:
    """Core banking service handling all banking operations"""
    
    def __init__(self):
        self.accounts = {}  # account_id -> Account object
        self.users = {}  # user_id -> User object
    
    def create_account(self, user, account_type: str = 'savings', initial_deposit: float = 0.0) -> Account:
        """Create a new account for a user"""
        account = Account(user.id, account_type, initial_deposit)
        self.accounts[account.id] = account
        user.add_account(account.id)
        return account
    
    def get_account(self, account_id: str) -> Account:
        """Get account by ID"""
        account = self.accounts.get(account_id)
        if not account:
            raise ValueError("Account not found")
        return account
    
    def get_account_by_number(self, account_number: str) -> Account:
        """Get account by account number"""
        for account in self.accounts.values():
            if account.account_number == account_number:
                return account
        raise ValueError("Account not found")
    
    def get_user_accounts(self, user_id: str) -> List[Account]:
        """Get all accounts for a user"""
        return [acc for acc in self.accounts.values() if acc.user_id == user_id]
    
    def deposit(self, account_id: str, amount: float, description: str = "Deposit") -> dict:
        """Process a deposit"""
        account = self.get_account(account_id)
        if account.status != 'active':
            raise ValueError(f"Account is {account.status}. Cannot perform deposit.")
        return account.deposit(amount, description)
    
    def withdraw(self, account_id: str, amount: float, description: str = "Withdrawal") -> dict:
        """Process a withdrawal"""
        account = self.get_account(account_id)
        if account.status != 'active':
            raise ValueError(f"Account is {account.status}. Cannot perform withdrawal.")
        return account.withdraw(amount, description)
    
    def transfer(self, from_account_id: str, to_account_number: str, amount: float, description: str = "Transfer") -> dict:
        """Process a transfer between accounts"""
        from_account = self.get_account(from_account_id)
        to_account = self.get_account_by_number(to_account_number)
        
        if from_account.status != 'active' or to_account.status != 'active':
            raise ValueError("One or both accounts are not active")
        
        return from_account.transfer(to_account, amount, description)
    
    def get_transaction_history(self, account_id: str, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get transaction history for an account"""
        account = self.get_account(account_id)
        return account.get_transaction_history(limit, offset)
    
    def get_account_summary(self, account_id: str) -> dict:
        """Get account summary"""
        account = self.get_account(account_id)
        return account.get_summary()
    
    def close_account(self, account_id: str) -> Account:
        """Close an account"""
        account = self.get_account(account_id)
        account.close()
        return account
    
    def freeze_account(self, account_id: str) -> Account:
        """Freeze an account"""
        account = self.get_account(account_id)
        account.freeze()
        return account
    
    def unfreeze_account(self, account_id: str) -> Account:
        """Unfreeze an account"""
        account = self.get_account(account_id)
        account.unfreeze()
        return account
    
    def get_user_total_balance(self, user_id: str) -> float:
        """Get total balance for a user across all accounts"""
        accounts = self.get_user_accounts(user_id)
        return sum(account.balance for account in accounts)