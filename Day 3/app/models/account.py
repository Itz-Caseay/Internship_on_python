import uuid
from datetime import datetime
from typing import List, Dict, Optional

class Account:
    """Account model representing a bank account"""
    
    ACCOUNT_TYPES = ['savings', 'checking', 'business']
    STATUSES = ['active', 'frozen', 'closed']
    
    def __init__(self, user_id: str, account_type: str = 'savings', initial_deposit: float = 0.0):
        if account_type not in self.ACCOUNT_TYPES:
            raise ValueError(f"Invalid account type. Must be one of: {self.ACCOUNT_TYPES}")
        
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.account_number = self._generate_account_number()
        self.account_type = account_type
        self.balance = initial_deposit
        self.currency = 'USD'
        self.status = 'active'
        self.transactions = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.overdraft_limit = 0.0
    
    def _generate_account_number(self) -> str:
        """Generate a unique account number"""
        prefix = 'ACC'
        timestamp = str(int(datetime.now().timestamp()))[-8:]
        random_part = str(uuid.uuid4().int)[:4]
        return f"{prefix}{timestamp}{random_part}"
    
    def deposit(self, amount: float, description: str = "Deposit") -> dict:
        """Deposit money into the account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.updated_at = datetime.now()
        
        transaction = {
            'id': str(uuid.uuid4()),
            'type': 'deposit',
            'amount': amount,
            'description': description,
            'balance': self.balance,
            'timestamp': datetime.now().isoformat()
        }
        
        self.transactions.append(transaction)
        return transaction
    
    def withdraw(self, amount: float, description: str = "Withdrawal") -> dict:
        """Withdraw money from the account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        available_balance = self.balance + self.overdraft_limit
        
        if amount > available_balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self.updated_at = datetime.now()
        
        transaction = {
            'id': str(uuid.uuid4()),
            'type': 'withdrawal',
            'amount': amount,
            'description': description,
            'balance': self.balance,
            'timestamp': datetime.now().isoformat()
        }
        
        self.transactions.append(transaction)
        return transaction
    
    def transfer(self, to_account, amount: float, description: str = "Transfer") -> dict:
        """Transfer money to another account"""
        if not isinstance(to_account, Account):
            raise ValueError("Invalid destination account")
        
        if self.id == to_account.id:
            raise ValueError("Cannot transfer to same account")
        
        # Withdraw from this account
        self.withdraw(amount, f"Transfer to {to_account.account_number}")
        
        # Deposit to destination account
        to_account.deposit(amount, f"Transfer from {self.account_number}")
        
        return {
            'from': self.account_number,
            'to': to_account.account_number,
            'amount': amount,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_transaction_history(self, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get transaction history"""
        return self.transactions[offset:offset + limit][::-1]  # Reverse for newest first
    
    def get_summary(self) -> dict:
        """Get account summary"""
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'status': self.status,
            'currency': self.currency,
            'total_transactions': len(self.transactions),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def freeze(self) -> None:
        """Freeze the account"""
        if self.status == 'closed':
            raise ValueError("Cannot freeze a closed account")
        self.status = 'frozen'
        self.updated_at = datetime.now()
    
    def unfreeze(self) -> None:
        """Unfreeze the account"""
        if self.status == 'closed':
            raise ValueError("Cannot unfreeze a closed account")
        self.status = 'active'
        self.updated_at = datetime.now()
    
    def close(self) -> None:
        """Close the account"""
        if self.balance > 0:
            raise ValueError("Cannot close account with positive balance. Withdraw all funds first.")
        self.status = 'closed'
        self.updated_at = datetime.now()
    
    def __repr__(self):
        return f"<Account {self.account_number} ({self.account_type})>"