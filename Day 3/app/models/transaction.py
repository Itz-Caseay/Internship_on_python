import uuid
from datetime import datetime
from typing import Optional

class Transaction:
    """Transaction model representing a financial transaction"""
    
    TRANSACTION_TYPES = ['deposit', 'withdrawal', 'transfer', 'fee', 'interest']
    STATUSES = ['pending', 'completed', 'failed']
    
    def __init__(self, account_id: str, transaction_type: str, amount: float, description: str = ""):
        if transaction_type not in self.TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type. Must be one of: {self.TRANSACTION_TYPES}")
        
        self.id = str(uuid.uuid4())
        self.account_id = account_id
        self.type = transaction_type
        self.amount = amount
        self.description = description
        self.status = 'completed'
        self.timestamp = datetime.now()
        self.reference = self._generate_reference()
        
        # Validate
        self.validate()
    
    def _generate_reference(self) -> str:
        """Generate a unique transaction reference"""
        prefix = 'TXN'
        timestamp = str(int(datetime.now().timestamp()))[-8:]
        random_part = str(uuid.uuid4().int)[:4]
        return f"{prefix}{timestamp}{random_part}"
    
    def validate(self) -> None:
        """Validate the transaction"""
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
    
    def mark_as_failed(self) -> None:
        """Mark transaction as failed"""
        self.status = 'failed'
    
    def mark_as_completed(self) -> None:
        """Mark transaction as completed"""
        self.status = 'completed'
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'reference': self.reference,
            'type': self.type,
            'amount': self.amount,
            'description': self.description,
            'status': self.status,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self):
        return f"<Transaction {self.reference} ({self.type})>"