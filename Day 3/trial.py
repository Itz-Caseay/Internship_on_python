#!/usr/bin/env python3
"""
🏦 Bank Simulator - Complete Banking Application with GUI
Features: Account management, Transactions, Transfers, Interest calculation, History
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import json
import os
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import threading
import time
import re

# ============================================================================
# DATA LAYER
# ============================================================================

class Customer:
    """Customer model representing a bank customer"""
    
    def __init__(self, 
                 first_name: str,
                 last_name: str,
                 email: str,
                 phone: str,
                 address: str = "",
                 date_of_birth: str = ""):
        
        self.id = self._generate_id()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.phone = phone.strip()
        self.address = address.strip()
        self.date_of_birth = date_of_birth
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_active = True
        self.account_ids = []
        
        self._validate()
    
    def _generate_id(self) -> str:
        """Generate a unique customer ID"""
        return f"CUST{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def _validate(self):
        """Validate customer data"""
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if not self.email:
            raise ValueError("Email is required")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
            raise ValueError("Invalid email format")
        if not self.phone:
            raise ValueError("Phone number is required")
    
    def get_full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def add_account(self, account_id: str):
        """Add an account to the customer"""
        if account_id not in self.account_ids:
            self.account_ids.append(account_id)
            self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'is_active': self.is_active,
            'account_ids': self.account_ids,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Customer':
        """Create customer from dictionary"""
        customer = cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address', ''),
            date_of_birth=data.get('date_of_birth', '')
        )
        customer.id = data['id']
        customer.is_active = data.get('is_active', True)
        customer.account_ids = data.get('account_ids', [])
        customer.created_at = datetime.fromisoformat(data['created_at'])
        customer.updated_at = datetime.fromisoformat(data['updated_at'])
        return customer

class Account:
    """Account model representing a bank account"""
    
    ACCOUNT_TYPES = ['Savings', 'Checking', 'Business', 'Investment']
    
    def __init__(self,
                 customer_id: str,
                 account_type: str = 'Savings',
                 initial_balance: float = 0.0,
                 currency: str = 'USD'):
        
        if account_type not in self.ACCOUNT_TYPES:
            raise ValueError(f"Invalid account type. Must be one of: {self.ACCOUNT_TYPES}")
        
        self.id = self._generate_id()
        self.customer_id = customer_id
        self.account_number = self._generate_account_number()
        self.account_type = account_type
        self.balance = initial_balance
        self.currency = currency
        self.status = 'Active'  # Active, Frozen, Closed
        self.interest_rate = self._get_interest_rate(account_type)
        self.overdraft_limit = 0.0
        self.transactions = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _generate_id(self) -> str:
        """Generate a unique account ID"""
        return f"ACC{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def _generate_account_number(self) -> str:
        """Generate a unique account number"""
        prefix = 'AC'
        timestamp = datetime.now().strftime('%Y%m%d')
        random_part = str(random.randint(10000, 99999))
        return f"{prefix}{timestamp}{random_part}"
    
    def _get_interest_rate(self, account_type: str) -> float:
        """Get interest rate based on account type"""
        rates = {
            'Savings': 0.035,  # 3.5%
            'Checking': 0.01,   # 1.0%
            'Business': 0.025,  # 2.5%
            'Investment': 0.05  # 5.0%
        }
        return rates.get(account_type, 0.0)
    
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
    
    def calculate_interest(self) -> float:
        """Calculate interest for the account"""
        if self.balance <= 0:
            return 0
        
        # Simple interest calculation (annual rate, monthly)
        monthly_rate = self.interest_rate / 12
        interest = self.balance * monthly_rate
        
        # Add interest to balance
        self.balance += interest
        self.updated_at = datetime.now()
        
        transaction = {
            'id': str(uuid.uuid4()),
            'type': 'interest',
            'amount': interest,
            'description': 'Monthly interest',
            'balance': self.balance,
            'timestamp': datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        
        return interest
    
    def get_transaction_history(self, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get transaction history"""
        return self.transactions[offset:offset + limit][::-1]
    
    def get_summary(self) -> dict:
        """Get account summary"""
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'status': self.status,
            'interest_rate': self.interest_rate,
            'total_transactions': len(self.transactions),
            'created_at': self.created_at.isoformat()
        }
    
    def freeze(self) -> None:
        """Freeze the account"""
        if self.status == 'Closed':
            raise ValueError("Cannot freeze a closed account")
        self.status = 'Frozen'
        self.updated_at = datetime.now()
    
    def unfreeze(self) -> None:
        """Unfreeze the account"""
        if self.status == 'Closed':
            raise ValueError("Cannot unfreeze a closed account")
        self.status = 'Active'
        self.updated_at = datetime.now()
    
    def close(self) -> None:
        """Close the account"""
        if self.balance > 0:
            raise ValueError("Cannot close account with positive balance. Withdraw all funds first.")
        self.status = 'Closed'
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'status': self.status,
            'interest_rate': self.interest_rate,
            'overdraft_limit': self.overdraft_limit,
            'transactions': self.transactions,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Account':
        """Create account from dictionary"""
        account = cls(
            customer_id=data['customer_id'],
            account_type=data['account_type'],
            initial_balance=data['balance'],
            currency=data.get('currency', 'USD')
        )
        account.id = data['id']
        account.account_number = data['account_number']
        account.status = data.get('status', 'Active')
        account.interest_rate = data.get('interest_rate', 0.0)
        account.overdraft_limit = data.get('overdraft_limit', 0.0)
        account.transactions = data.get('transactions', [])
        account.created_at = datetime.fromisoformat(data['created_at'])
        account.updated_at = datetime.fromisoformat(data['updated_at'])
        return account

class Loan:
    """Loan model representing a bank loan"""
    
    LOAN_TYPES = ['Personal', 'Home', 'Auto', 'Business']
    LOAN_STATUSES = ['Pending', 'Approved', 'Rejected', 'Active', 'Paid']
    
    def __init__(self,
                 customer_id: str,
                 amount: float,
                 loan_type: str = 'Personal',
                 term_months: int = 12,
                 interest_rate: float = 0.08):
        
        if loan_type not in self.LOAN_TYPES:
            raise ValueError(f"Invalid loan type. Must be one of: {self.LOAN_TYPES}")
        
        self.id = self._generate_id()
        self.customer_id = customer_id
        self.loan_number = self._generate_loan_number()
        self.loan_type = loan_type
        self.amount = amount
        self.interest_rate = interest_rate
        self.term_months = term_months
        self.status = 'Pending'
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.payments = []
        self.remaining_balance = amount
        self.approval_date = None
        self.completion_date = None
    
    def _generate_id(self) -> str:
        return f"LOAN{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def _generate_loan_number(self) -> str:
        prefix = 'LN'
        timestamp = datetime.now().strftime('%Y%m%d')
        random_part = str(random.randint(10000, 99999))
        return f"{prefix}{timestamp}{random_part}"
    
    def calculate_monthly_payment(self) -> float:
        """Calculate monthly payment using amortization formula"""
        if self.amount <= 0:
            return 0
        
        monthly_rate = self.interest_rate / 12
        if monthly_rate == 0:
            return self.amount / self.term_months
        
        payment = self.amount * (monthly_rate * (1 + monthly_rate) ** self.term_months) / \
                 ((1 + monthly_rate) ** self.term_months - 1)
        return payment
    
    def make_payment(self, amount: float) -> dict:
        """Make a loan payment"""
        if self.status not in ['Approved', 'Active']:
            raise ValueError("Loan is not active")
        
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        
        if amount > self.remaining_balance:
            raise ValueError("Payment exceeds remaining balance")
        
        self.remaining_balance -= amount
        self.updated_at = datetime.now()
        
        payment = {
            'id': str(uuid.uuid4()),
            'amount': amount,
            'date': datetime.now().isoformat(),
            'remaining_balance': self.remaining_balance
        }
        self.payments.append(payment)
        
        if self.remaining_balance <= 0:
            self.status = 'Paid'
            self.completion_date = datetime.now()
        
        return payment
    
    def approve(self) -> None:
        """Approve the loan"""
        if self.status != 'Pending':
            raise ValueError("Loan must be pending to approve")
        
        self.status = 'Active'
        self.approval_date = datetime.now()
        self.updated_at = datetime.now()
    
    def reject(self) -> None:
        """Reject the loan"""
        if self.status != 'Pending':
            raise ValueError("Loan must be pending to reject")
        
        self.status = 'Rejected'
        self.updated_at = datetime.now()
    
    def get_summary(self) -> dict:
        """Get loan summary"""
        return {
            'id': self.id,
            'loan_number': self.loan_number,
            'loan_type': self.loan_type,
            'amount': self.amount,
            'remaining_balance': self.remaining_balance,
            'interest_rate': self.interest_rate,
            'term_months': self.term_months,
            'monthly_payment': self.calculate_monthly_payment(),
            'status': self.status,
            'payments_made': len(self.payments),
            'created_at': self.created_at.isoformat()
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'loan_number': self.loan_number,
            'loan_type': self.loan_type,
            'amount': self.amount,
            'interest_rate': self.interest_rate,
            'term_months': self.term_months,
            'status': self.status,
            'remaining_balance': self.remaining_balance,
            'payments': self.payments,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Loan':
        """Create loan from dictionary"""
        loan = cls(
            customer_id=data['customer_id'],
            amount=data['amount'],
            loan_type=data['loan_type'],
            term_months=data['term_months'],
            interest_rate=data.get('interest_rate', 0.08)
        )
        loan.id = data['id']
        loan.loan_number = data['loan_number']
        loan.status = data.get('status', 'Pending')
        loan.remaining_balance = data.get('remaining_balance', data['amount'])
        loan.payments = data.get('payments', [])
        loan.created_at = datetime.fromisoformat(data['created_at'])
        loan.updated_at = datetime.fromisoformat(data['updated_at'])
        if data.get('approval_date'):
            loan.approval_date = datetime.fromisoformat(data['approval_date'])
        if data.get('completion_date'):
            loan.completion_date = datetime.fromisoformat(data['completion_date'])
        return loan

# ============================================================================
# STORAGE HANDLER
# ============================================================================

class StorageHandler:
    """Handles data persistence"""
    
    def __init__(self):
        self.data_dir = Path.home() / ".bank_simulator"
        self.data_dir.mkdir(exist_ok=True)
        
        self.customers_file = self.data_dir / "customers.json"
        self.accounts_file = self.data_dir / "accounts.json"
        self.loans_file = self.data_dir / "loans.json"
    
    def save_data(self, filename: Path, data: List[dict]) -> bool:
        """Save data to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_data(self, filename: Path) -> List[dict]:
        """Load data from file"""
        if not filename.exists():
            return []
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def save_customers(self, customers: List[dict]) -> bool:
        return self.save_data(self.customers_file, customers)
    
    def load_customers(self) -> List[dict]:
        return self.load_data(self.customers_file)
    
    def save_accounts(self, accounts: List[dict]) -> bool:
        return self.save_data(self.accounts_file, accounts)
    
    def load_accounts(self) -> List[dict]:
        return self.load_data(self.accounts_file)
    
    def save_loans(self, loans: List[dict]) -> bool:
        return self.save_data(self.loans_file, loans)
    
    def load_loans(self) -> List[dict]:
        return self.load_data(self.loans_file)

# ============================================================================
# SERVICE LAYER
# ============================================================================

class BankingService:
    """Core banking service"""
    
    def __init__(self):
        self.storage = StorageHandler()
        self.customers: Dict[str, Customer] = {}
        self.accounts: Dict[str, Account] = {}
        self.loans: Dict[str, Loan] = {}
        
        self._load_data()
    
    def _load_data(self):
        """Load all data from storage"""
        # Load customers
        customer_data = self.storage.load_customers()
        for data in customer_data:
            try:
                customer = Customer.from_dict(data)
                self.customers[customer.id] = customer
            except Exception:
                continue
        
        # Load accounts
        account_data = self.storage.load_accounts()
        for data in account_data:
            try:
                account = Account.from_dict(data)
                self.accounts[account.id] = account
            except Exception:
                continue
        
        # Load loans
        loan_data = self.storage.load_loans()
        for data in loan_data:
            try:
                loan = Loan.from_dict(data)
                self.loans[loan.id] = loan
            except Exception:
                continue
    
    def _save_all(self):
        """Save all data to storage"""
        customer_data = [c.to_dict() for c in self.customers.values()]
        self.storage.save_customers(customer_data)
        
        account_data = [a.to_dict() for a in self.accounts.values()]
        self.storage.save_accounts(account_data)
        
        loan_data = [l.to_dict() for l in self.loans.values()]
        self.storage.save_loans(loan_data)
    
    # ========================================================================
    # Customer Operations
    # ========================================================================
    
    def add_customer(self, **kwargs) -> Customer:
        """Add a new customer"""
        customer = Customer(**kwargs)
        self.customers[customer.id] = customer
        self._save_all()
        return customer
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID"""
        return self.customers.get(customer_id)
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return sorted(self.customers.values(), key=lambda x: x.get_full_name())
    
    def search_customers(self, query: str) -> List[Customer]:
        """Search customers"""
        query = query.lower().strip()
        if not query:
            return []
        
        results = []
        for customer in self.customers.values():
            if (query in customer.first_name.lower() or 
                query in customer.last_name.lower() or
                query in customer.email.lower() or
                query in customer.phone):
                results.append(customer)
        return results
    
    # ========================================================================
    # Account Operations
    # ========================================================================
    
    def create_account(self, customer_id: str, account_type: str = 'Savings', 
                      initial_balance: float = 0.0) -> Account:
        """Create a new account for a customer"""
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        account = Account(customer_id, account_type, initial_balance)
        self.accounts[account.id] = account
        customer.add_account(account.id)
        self._save_all()
        return account
    
    def get_account(self, account_id: str) -> Optional[Account]:
        """Get an account by ID"""
        return self.accounts.get(account_id)
    
    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """Get an account by account number"""
        for account in self.accounts.values():
            if account.account_number == account_number:
                return account
        return None
    
    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        """Get all accounts for a customer"""
        customer = self.get_customer(customer_id)
        if not customer:
            return []
        
        accounts = []
        for acc_id in customer.account_ids:
            account = self.accounts.get(acc_id)
            if account:
                accounts.append(account)
        return sorted(accounts, key=lambda x: x.account_type)
    
    def deposit(self, account_id: str, amount: float, description: str = "Deposit") -> dict:
        """Deposit money to an account"""
        account = self.get_account(account_id)
        if not account:
            raise ValueError("Account not found")
        
        if account.status != 'Active':
            raise ValueError(f"Cannot deposit to {account.status} account")
        
        transaction = account.deposit(amount, description)
        self._save_all()
        return transaction
    
    def withdraw(self, account_id: str, amount: float, description: str = "Withdrawal") -> dict:
        """Withdraw money from an account"""
        account = self.get_account(account_id)
        if not account:
            raise ValueError("Account not found")
        
        if account.status != 'Active':
            raise ValueError(f"Cannot withdraw from {account.status} account")
        
        transaction = account.withdraw(amount, description)
        self._save_all()
        return transaction
    
    def transfer(self, from_account_id: str, to_account_number: str, 
                amount: float, description: str = "Transfer") -> dict:
        """Transfer money between accounts"""
        from_account = self.get_account(from_account_id)
        if not from_account:
            raise ValueError("Source account not found")
        
        if from_account.status != 'Active':
            raise ValueError(f"Source account is {from_account.status}")
        
        to_account = self.get_account_by_number(to_account_number)
        if not to_account:
            raise ValueError("Destination account not found")
        
        if to_account.status != 'Active':
            raise ValueError(f"Destination account is {to_account.status}")
        
        transfer = from_account.transfer(to_account, amount, description)
        self._save_all()
        return transfer
    
    def get_account_transactions(self, account_id: str, limit: int = 50) -> List[dict]:
        """Get transaction history for an account"""
        account = self.get_account(account_id)
        if not account:
            return []
        return account.get_transaction_history(limit)
    
    def get_account_summary(self, account_id: str) -> dict:
        """Get account summary"""
        account = self.get_account(account_id)
        if not account:
            return {}
        return account.get_summary()
    
    def freeze_account(self, account_id: str) -> bool:
        """Freeze an account"""
        account = self.get_account(account_id)
        if not account:
            return False
        account.freeze()
        self._save_all()
        return True
    
    def unfreeze_account(self, account_id: str) -> bool:
        """Unfreeze an account"""
        account = self.get_account(account_id)
        if not account:
            return False
        account.unfreeze()
        self._save_all()
        return True
    
    def close_account(self, account_id: str) -> bool:
        """Close an account"""
        account = self.get_account(account_id)
        if not account:
            return False
        account.close()
        self._save_all()
        return True
    
    def calculate_interest_for_all(self) -> int:
        """Calculate interest for all eligible accounts"""
        count = 0
        for account in self.accounts.values():
            if account.status == 'Active' and account.balance > 0:
                account.calculate_interest()
                count += 1
        self._save_all()
        return count
    
    # ========================================================================
    # Loan Operations
    # ========================================================================
    
    def apply_for_loan(self, customer_id: str, amount: float, 
                       loan_type: str = 'Personal', 
                       term_months: int = 12) -> Loan:
        """Apply for a loan"""
        customer = self.get_customer(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        loan = Loan(customer_id, amount, loan_type, term_months)
        self.loans[loan.id] = loan
        self._save_all()
        return loan
    
    def get_loan(self, loan_id: str) -> Optional[Loan]:
        """Get a loan by ID"""
        return self.loans.get(loan_id)
    
    def get_customer_loans(self, customer_id: str) -> List[Loan]:
        """Get all loans for a customer"""
        return [l for l in self.loans.values() if l.customer_id == customer_id]
    
    def approve_loan(self, loan_id: str) -> bool:
        """Approve a loan"""
        loan = self.get_loan(loan_id)
        if not loan:
            return False
        loan.approve()
        self._save_all()
        return True
    
    def reject_loan(self, loan_id: str) -> bool:
        """Reject a loan"""
        loan = self.get_loan(loan_id)
        if not loan:
            return False
        loan.reject()
        self._save_all()
        return True
    
    def make_loan_payment(self, loan_id: str, amount: float) -> dict:
        """Make a loan payment"""
        loan = self.get_loan(loan_id)
        if not loan:
            raise ValueError("Loan not found")
        
        payment = loan.make_payment(amount)
        self._save_all()
        return payment
    
    def get_loan_summary(self, loan_id: str) -> dict:
        """Get loan summary"""
        loan = self.get_loan(loan_id)
        if not loan:
            return {}
        return loan.get_summary()
    
    # ========================================================================
    # Statistics
    # ========================================================================
    
    def get_total_balance(self) -> float:
        """Get total balance across all accounts"""
        return sum(a.balance for a in self.accounts.values())
    
    def get_total_loans(self) -> float:
        """Get total outstanding loans"""
        return sum(l.remaining_balance for l in self.loans.values() 
                  if l.status in ['Approved', 'Active'])
    
    def get_customer_count(self) -> int:
        """Get number of customers"""
        return len(self.customers)
    
    def get_account_count(self) -> int:
        """Get number of accounts"""
        return len(self.accounts)
    
    def get_loan_count(self) -> int:
        """Get number of loans"""
        return len(self.loans)

# ============================================================================
# UI LAYER - MAIN APPLICATION
# ============================================================================

class BankSimulatorApp:
    """Main application with beautiful UI"""
    
    COLORS = {
        'primary': '#1565C0',
        'primary_dark': '#0D47A1',
        'primary_light': '#64B5F6',
        'secondary': '#FF6F00',
        'success': '#2E7D32',
        'danger': '#C62828',
        'warning': '#F57F17',
        'info': '#00838F',
        'dark': '#1A1A2E',
        'light': '#F5F5F5',
        'white': '#FFFFFF',
        'gray': '#757575',
        'background': '#E8EAF6',
        'card': '#FFFFFF',
        'border': '#DEE2E6',
        'shadow': '#0000001A',
        'gold': '#FFD700'
    }
    
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 11),
        'body_bold': ('Segoe UI', 11, 'bold'),
        'small': ('Segoe UI', 9),
        'small_bold': ('Segoe UI', 9, 'bold'),
        'mono': ('Consolas', 10)
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Bank Simulator")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        self.root.configure(bg=self.COLORS['background'])
        
        # Initialize service
        self.service = BankingService()
        
        # State
        self.current_customer_id = None
        self.current_account_id = None
        self.current_loan_id = None
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._load_data()
        
        # Center window
        self._center_window()
        
        # Demo data
        self._create_demo_data()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Treeview',
                       background=self.COLORS['white'],
                       foreground=self.COLORS['dark'],
                       rowheight=35,
                       font=self.FONTS['body'])
        style.configure('Treeview.Heading',
                       background=self.COLORS['primary'],
                       foreground=self.COLORS['white'],
                       font=self.FONTS['body_bold'])
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.COLORS['background'])
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self._create_header()
        
        # Content (split into 3 sections)
        self.content_frame = tk.Frame(self.main_container, bg=self.COLORS['background'])
        self.content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left: Customers list
        self._create_customer_list()
        
        # Center: Accounts/Transactions
        self._create_account_panel()
        
        # Right: Details
        self._create_details_panel()
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create the header"""
        header = tk.Frame(self.main_container, bg=self.COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Title
        title = tk.Label(header,
                        text="🏦 Bank Simulator",
                        font=self.FONTS['title'],
                        bg=self.COLORS['primary'],
                        fg=self.COLORS['white'])
        title.pack(side='left', padx=20, pady=15)
        
        # Stats
        stats = tk.Frame(header, bg=self.COLORS['primary'])
        stats.pack(side='right', padx=20)
        
        self.stats_total = tk.Label(stats,
                                   text="Total: $0.00",
                                   font=self.FONTS['body_bold'],
                                   bg=self.COLORS['primary'],
                                   fg=self.COLORS['white'])
        self.stats_total.pack(side='left', padx=10)
        
        self.stats_customers = tk.Label(stats,
                                       text="👥 0",
                                       font=self.FONTS['body'],
                                       bg=self.COLORS['primary'],
                                       fg=self.COLORS['white'])
        self.stats_customers.pack(side='left', padx=10)
        
        # Buttons
        btn_frame = tk.Frame(stats, bg=self.COLORS['primary'])
        btn_frame.pack(side='left', padx=10)
        
        add_customer_btn = tk.Button(btn_frame,
                                    text="➕ Add Customer",
                                    font=self.FONTS['body_bold'],
                                    bg=self.COLORS['success'],
                                    fg=self.COLORS['white'],
                                    relief='flat',
                                    padx=15,
                                    pady=5,
                                    cursor='hand2',
                                    command=self._add_customer)
        add_customer_btn.pack(side='left', padx=5)
        self._add_hover_effect(add_customer_btn, self.COLORS['success'], '#1B5E20')
        
        interest_btn = tk.Button(btn_frame,
                                text="💰 Calculate Interest",
                                font=self.FONTS['body'],
                                bg=self.COLORS['info'],
                                fg=self.COLORS['white'],
                                relief='flat',
                                padx=15,
                                pady=5,
                                cursor='hand2',
                                command=self._calculate_interest)
        interest_btn.pack(side='left', padx=5)
        self._add_hover_effect(interest_btn, self.COLORS['info'], '#006064')
        
        refresh_btn = tk.Button(btn_frame,
                               text="🔄 Refresh",
                               font=self.FONTS['body'],
                               bg=self.COLORS['secondary'],
                               fg=self.COLORS['white'],
                               relief='flat',
                               padx=15,
                               pady=5,
                               cursor='hand2',
                               command=self._refresh_data)
        refresh_btn.pack(side='left', padx=5)
        self._add_hover_effect(refresh_btn, self.COLORS['secondary'], '#E65100')
    
    def _create_customer_list(self):
        """Create the customer list panel"""
        left_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        left_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Header
        tk.Label(left_panel,
                text="👥 Customers",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(anchor='w', padx=15, pady=10)
        
        # Search
        search_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        search_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._search_customers())
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        search_entry.pack(fill='x', ipady=5)
        search_entry.insert(0, "🔍 Search customers...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "🔍 Search customers..." else None)
        
        # Customer tree
        tree_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.customer_tree = ttk.Treeview(tree_frame,
                                         columns=('name', 'email', 'phone'),
                                         show='headings',
                                         yscrollcommand=scrollbar.set,
                                         selectmode='browse')
        
        self.customer_tree.heading('name', text='Name', anchor='w')
        self.customer_tree.heading('email', text='Email', anchor='w')
        self.customer_tree.heading('phone', text='Phone', anchor='w')
        
        self.customer_tree.column('name', width=150)
        self.customer_tree.column('email', width=150)
        self.customer_tree.column('phone', width=100)
        
        self.customer_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.customer_tree.yview)
        
        self.customer_tree.bind('<<TreeviewSelect>>', self._on_customer_select)
    
    def _create_account_panel(self):
        """Create the accounts panel"""
        center_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        center_panel.pack(side='left', fill='both', expand=True, padx=5)
        center_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Accounts section
        acc_header = tk.Frame(center_panel, bg=self.COLORS['white'])
        acc_header.pack(fill='x', padx=15, pady=10)
        
        tk.Label(acc_header,
                text="💰 Accounts",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        acc_buttons = tk.Frame(acc_header, bg=self.COLORS['white'])
        acc_buttons.pack(side='right')
        
        tk.Button(acc_buttons,
                 text="➕ New Account",
                 font=self.FONTS['small'],
                 bg=self.COLORS['success'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=10,
                 pady=3,
                 cursor='hand2',
                 command=self._create_account).pack(side='left', padx=2)
        self._add_hover_effect(acc_buttons.winfo_children()[-1], self.COLORS['success'], '#1B5E20')
        
        # Account tree
        acc_tree_frame = tk.Frame(center_panel, bg=self.COLORS['white'])
        acc_tree_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        acc_scroll = ttk.Scrollbar(acc_tree_frame)
        acc_scroll.pack(side='right', fill='y')
        
        self.account_tree = ttk.Treeview(acc_tree_frame,
                                        columns=('number', 'type', 'balance', 'status'),
                                        show='headings',
                                        yscrollcommand=acc_scroll.set,
                                        height=5,
                                        selectmode='browse')
        
        self.account_tree.heading('number', text='Account', anchor='w')
        self.account_tree.heading('type', text='Type', anchor='w')
        self.account_tree.heading('balance', text='Balance', anchor='w')
        self.account_tree.heading('status', text='Status', anchor='w')
        
        self.account_tree.column('number', width=120)
        self.account_tree.column('type', width=80)
        self.account_tree.column('balance', width=100)
        self.account_tree.column('status', width=80)
        
        self.account_tree.pack(fill='x', expand=True)
        acc_scroll.config(command=self.account_tree.yview)
        self.account_tree.bind('<<TreeviewSelect>>', self._on_account_select)
        
        # Transaction section
        tx_header = tk.Frame(center_panel, bg=self.COLORS['white'])
        tx_header.pack(fill='x', padx=15, pady=(10, 5))
        
        tk.Label(tx_header,
                text="📋 Recent Transactions",
                font=self.FONTS['subheading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        # Transaction buttons
        tx_buttons = tk.Frame(tx_header, bg=self.COLORS['white'])
        tx_buttons.pack(side='right')
        
        tk.Button(tx_buttons,
                 text="💵 Deposit",
                 font=self.FONTS['small'],
                 bg=self.COLORS['success'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=10,
                 pady=3,
                 cursor='hand2',
                 command=self._deposit).pack(side='left', padx=2)
        self._add_hover_effect(tx_buttons.winfo_children()[-1], self.COLORS['success'], '#1B5E20')
        
        tk.Button(tx_buttons,
                 text="💸 Withdraw",
                 font=self.FONTS['small'],
                 bg=self.COLORS['warning'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=10,
                 pady=3,
                 cursor='hand2',
                 command=self._withdraw).pack(side='left', padx=2)
        self._add_hover_effect(tx_buttons.winfo_children()[-1], self.COLORS['warning'], '#E65100')
        
        tk.Button(tx_buttons,
                 text="🔄 Transfer",
                 font=self.FONTS['small'],
                 bg=self.COLORS['info'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=10,
                 pady=3,
                 cursor='hand2',
                 command=self._transfer).pack(side='left', padx=2)
        self._add_hover_effect(tx_buttons.winfo_children()[-1], self.COLORS['info'], '#006064')
        
        # Transaction list
        tx_frame = tk.Frame(center_panel, bg=self.COLORS['white'])
        tx_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        tx_scroll = ttk.Scrollbar(tx_frame)
        tx_scroll.pack(side='right', fill='y')
        
        self.transaction_tree = ttk.Treeview(tx_frame,
                                            columns=('date', 'type', 'amount', 'description', 'balance'),
                                            show='headings',
                                            yscrollcommand=tx_scroll.set,
                                            height=8)
        
        self.transaction_tree.heading('date', text='Date', anchor='w')
        self.transaction_tree.heading('type', text='Type', anchor='w')
        self.transaction_tree.heading('amount', text='Amount', anchor='e')
        self.transaction_tree.heading('description', text='Description', anchor='w')
        self.transaction_tree.heading('balance', text='Balance', anchor='e')
        
        self.transaction_tree.column('date', width=120)
        self.transaction_tree.column('type', width=80)
        self.transaction_tree.column('amount', width=100)
        self.transaction_tree.column('description', width=200)
        self.transaction_tree.column('balance', width=100)
        
        self.transaction_tree.pack(fill='both', expand=True)
        tx_scroll.config(command=self.transaction_tree.yview)
    
    def _create_details_panel(self):
        """Create the details panel"""
        right_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        right_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Header
        header_frame = tk.Frame(right_panel, bg=self.COLORS['white'])
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame,
                text="📋 Details",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        # Content with scrollbar
        details_container = tk.Frame(right_panel, bg=self.COLORS['white'])
        details_container.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        canvas = tk.Canvas(details_container, bg=self.COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_container, orient='vertical', command=canvas.yview)
        
        self.details_frame = tk.Frame(canvas, bg=self.COLORS['white'])
        self.details_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=self.details_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial details
        self._show_empty_details()
    
    def _create_status_bar(self):
        """Create the status bar"""
        status = tk.Frame(self.main_container, bg=self.COLORS['dark'], height=30)
        status.pack(side='bottom', fill='x')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status,
                                     text="✅ Ready",
                                     font=self.FONTS['small'],
                                     bg=self.COLORS['dark'],
                                     fg=self.COLORS['white'],
                                     anchor='w')
        self.status_label.pack(side='left', padx=10)
        
        self.status_time = tk.Label(status,
                                    text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    font=self.FONTS['small'],
                                    bg=self.COLORS['dark'],
                                    fg=self.COLORS['white'],
                                    anchor='e')
        self.status_time.pack(side='right', padx=10)
        
        # Update time
        self._update_time()
    
    def _update_time(self):
        """Update status bar time"""
        self.status_time.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.root.after(1000, self._update_time)
    
    # ========================================================================
    # UI Helper Methods
    # ========================================================================
    
    def _add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to a button"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button['background'] = hover_color
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button['background'] = normal_color
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def _set_status(self, message, is_error=False):
        """Set status bar message"""
        color = self.COLORS['danger'] if is_error else self.COLORS['white']
        self.status_label.config(text=f"{'❌' if is_error else '✅'} {message}", fg=color)
    
    def _clear_tree(self, tree):
        """Clear a treeview"""
        for item in tree.get_children():
            tree.delete(item)
    
    # ========================================================================
    # Data Loading Methods
    # ========================================================================
    
    def _load_data(self):
        """Load and display all data"""
        self._load_customers()
        self._load_customer_accounts()
        self._update_stats()
    
    def _load_customers(self):
        """Load customers into treeview"""
        self._clear_tree(self.customer_tree)
        
        customers = self.service.get_all_customers()
        for customer in customers:
            self.customer_tree.insert('', 'end',
                                     values=(customer.get_full_name(), 
                                            customer.email, 
                                            customer.phone),
                                     tags=(customer.id,))
    
    def _load_customer_accounts(self):
        """Load accounts for selected customer"""
        self._clear_tree(self.account_tree)
        self._clear_tree(self.transaction_tree)
        
        if not self.current_customer_id:
            return
        
        accounts = self.service.get_customer_accounts(self.current_customer_id)
        for account in accounts:
            self.account_tree.insert('', 'end',
                                    values=(account.account_number,
                                           account.account_type,
                                           f"${account.balance:,.2f}",
                                           account.status),
                                    tags=(account.id,))
    
    def _load_transactions(self, account_id: str):
        """Load transactions for an account"""
        self._clear_tree(self.transaction_tree)
        
        if not account_id:
            return
        
        transactions = self.service.get_account_transactions(account_id, 20)
        for tx in transactions:
            amount = tx['amount']
            amount_str = f"+${amount:,.2f}" if tx['type'] == 'deposit' else f"-${amount:,.2f}"
            self.transaction_tree.insert('', 'end',
                                        values=(tx['timestamp'][:16],
                                               tx['type'].capitalize(),
                                               amount_str,
                                               tx['description'][:30],
                                               f"${tx['balance']:,.2f}"))
    
    def _update_stats(self):
        """Update statistics in header"""
        total = self.service.get_total_balance()
        customers = self.service.get_customer_count()
        
        self.stats_total.config(text=f"Total: ${total:,.2f}")
        self.stats_customers.config(text=f"👥 {customers}")
    
    # ========================================================================
    # Event Handlers
    # ========================================================================
    
    def _on_customer_select(self, event):
        """Handle customer selection"""
        if not self.customer_tree.selection():
            return
        
        item = self.customer_tree.selection()[0]
        customer_id = self.customer_tree.item(item, 'tags')[0]
        self.current_customer_id = customer_id
        
        customer = self.service.get_customer(customer_id)
        if customer:
            self._show_customer_details(customer)
            self._load_customer_accounts()
            self._set_status(f"Selected customer: {customer.get_full_name()}")
    
    def _on_account_select(self, event):
        """Handle account selection"""
        if not self.account_tree.selection():
            return
        
        item = self.account_tree.selection()[0]
        account_id = self.account_tree.item(item, 'tags')[0]
        self.current_account_id = account_id
        
        account = self.service.get_account(account_id)
        if account:
            self._show_account_details(account)
            self._load_transactions(account_id)
            self._set_status(f"Selected account: {account.account_number}")
    
    def _search_customers(self):
        """Search customers"""
        query = self.search_var.get()
        if query == "🔍 Search customers...":
            query = ""
        
        self._clear_tree(self.customer_tree)
        
        if query:
            results = self.service.search_customers(query)
        else:
            results = self.service.get_all_customers()
        
        for customer in results:
            self.customer_tree.insert('', 'end',
                                     values=(customer.get_full_name(),
                                            customer.email,
                                            customer.phone),
                                     tags=(customer.id,))
    
    # ========================================================================
    # Details Display Methods
    # ========================================================================
    
    def _show_empty_details(self):
        """Show empty details message"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.details_frame,
                text="No Selection",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['gray']).pack(pady=50)
        
        tk.Label(self.details_frame,
                text="Select a customer to view details",
                font=self.FONTS['body'],
                bg=self.COLORS['white'],
                fg=self.COLORS['gray']).pack()
    
    def _show_customer_details(self, customer: Customer):
        """Show customer details"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Name
        tk.Label(self.details_frame,
                text=customer.get_full_name(),
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(anchor='w', pady=(0, 10))
        
        # Details in grid
        details = [
            ("ID", customer.id),
            ("Email", customer.email),
            ("Phone", customer.phone),
            ("Address", customer.address or "Not specified"),
            ("Date of Birth", customer.date_of_birth or "Not specified"),
            ("Accounts", str(len(customer.account_ids))),
            ("Created", customer.created_at.strftime('%Y-%m-%d %H:%M')),
            ("Status", "Active" if customer.is_active else "Inactive")
        ]
        
        for label, value in details:
            frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame,
                    text=f"{label}:",
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['gray'],
                    width=12,
                    anchor='w').pack(side='left')
            
            tk.Label(frame,
                    text=value,
                    font=self.FONTS['body'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark'],
                    anchor='w').pack(side='left')
        
        # Actions
        btn_frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', pady=(15, 0))
        
        tk.Button(btn_frame,
                 text="🏦 Create Account",
                 font=self.FONTS['body'],
                 bg=self.COLORS['success'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=self._create_account).pack(side='left', padx=2)
        
        tk.Button(btn_frame,
                 text="💰 Apply for Loan",
                 font=self.FONTS['body'],
                 bg=self.COLORS['warning'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=self._apply_loan).pack(side='left', padx=2)
        
        tk.Button(btn_frame,
                 text="✏️ Edit",
                 font=self.FONTS['body'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=lambda: self._edit_customer(customer.id)).pack(side='left', padx=2)
        
        # Loans section
        loans = self.service.get_customer_loans(customer.id)
        if loans:
            tk.Label(self.details_frame,
                    text="\n📋 Loans",
                    font=self.FONTS['subheading'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).pack(anchor='w', pady=(15, 5))
            
            for loan in loans:
                tk.Label(self.details_frame,
                        text=f"  • {loan.loan_type}: ${loan.remaining_balance:,.2f} ({loan.status})",
                        font=self.FONTS['body'],
                        bg=self.COLORS['white'],
                        fg=self.COLORS['dark']).pack(anchor='w')
    
    def _show_account_details(self, account: Account):
        """Show account details in the details panel"""
        # For now, just update the account tree selection
        # Detailed account info is already in the account panel
        pass
    
    # ========================================================================
    # Customer Operations
    # ========================================================================
    
    def _add_customer(self):
        """Add a new customer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Customer")
        dialog.geometry("500x550")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"500x550+{x}+{y}")
        
        tk.Label(dialog,
                text="👤 Add New Customer",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        fields = [
            ('first_name', "First Name *"),
            ('last_name', "Last Name *"),
            ('email', "Email *"),
            ('phone', "Phone *"),
            ('address', "Address"),
            ('date_of_birth', "Date of Birth (YYYY-MM-DD)")
        ]
        
        entries = {}
        
        for i, (field, label) in enumerate(fields):
            tk.Label(form,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            var = tk.StringVar()
            entry = tk.Entry(form,
                            textvariable=var,
                            font=self.FONTS['body'],
                            bg=self.COLORS['light'],
                            relief='flat',
                            bd=0,
                            highlightthickness=1,
                            highlightcolor=self.COLORS['primary'])
            entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
            entries[field] = var
        
        form.grid_columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def save_customer():
            try:
                customer = self.service.add_customer(
                    first_name=entries['first_name'].get().strip(),
                    last_name=entries['last_name'].get().strip(),
                    email=entries['email'].get().strip(),
                    phone=entries['phone'].get().strip(),
                    address=entries['address'].get().strip(),
                    date_of_birth=entries['date_of_birth'].get().strip()
                )
                
                self._load_data()
                dialog.destroy()
                messagebox.showinfo("Success", f"Added customer: {customer.get_full_name()}")
                self._set_status(f"Added customer: {customer.get_full_name()}")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {e}")
        
        tk.Button(btn_frame,
                 text="💾 Save Customer",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=save_customer).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    def _edit_customer(self, customer_id: str):
        """Edit a customer"""
        customer = self.service.get_customer(customer_id)
        if not customer:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Customer")
        dialog.geometry("500x550")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (550 // 2)
        dialog.geometry(f"500x550+{x}+{y}")
        
        tk.Label(dialog,
                text=f"✏️ Edit Customer: {customer.get_full_name()}",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        fields = [
            ('first_name', "First Name *"),
            ('last_name', "Last Name *"),
            ('email', "Email *"),
            ('phone', "Phone *"),
            ('address', "Address"),
            ('date_of_birth', "Date of Birth (YYYY-MM-DD)")
        ]
        
        entries = {}
        
        for i, (field, label) in enumerate(fields):
            tk.Label(form,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            var = tk.StringVar(value=getattr(customer, field))
            entry = tk.Entry(form,
                            textvariable=var,
                            font=self.FONTS['body'],
                            bg=self.COLORS['light'],
                            relief='flat',
                            bd=0,
                            highlightthickness=1,
                            highlightcolor=self.COLORS['primary'])
            entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
            entries[field] = var
        
        form.grid_columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def update_customer():
            try:
                # Update customer attributes
                for field in fields:
                    field_name = field[0]
                    value = entries[field_name].get().strip()
                    setattr(customer, field_name, value)
                
                customer.updated_at = datetime.now()
                self.service._save_all()
                
                self._load_data()
                dialog.destroy()
                messagebox.showinfo("Success", f"Updated customer: {customer.get_full_name()}")
                self._set_status(f"Updated customer: {customer.get_full_name()}")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update customer: {e}")
        
        tk.Button(btn_frame,
                 text="💾 Update Customer",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=update_customer).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    # ========================================================================
    # Account Operations
    # ========================================================================
    
    def _create_account(self):
        """Create a new account for selected customer"""
        if not self.current_customer_id:
            messagebox.showwarning("Warning", "Please select a customer first")
            return
        
        customer = self.service.get_customer(self.current_customer_id)
        if not customer:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Account")
        dialog.geometry("400x400")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"400x400+{x}+{y}")
        
        tk.Label(dialog,
                text=f"🏦 Create Account for {customer.get_full_name()}",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        # Account type
        tk.Label(form,
                text="Account Type:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        account_type_var = tk.StringVar(value="Savings")
        account_type_menu = ttk.Combobox(form,
                                        textvariable=account_type_var,
                                        values=Account.ACCOUNT_TYPES,
                                        font=self.FONTS['body'],
                                        state='readonly')
        account_type_menu.grid(row=0, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        # Initial balance
        tk.Label(form,
                text="Initial Balance:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        balance_var = tk.StringVar(value="0.00")
        balance_entry = tk.Entry(form,
                                textvariable=balance_var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
        balance_entry.grid(row=1, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        # Currency
        tk.Label(form,
                text="Currency:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=2, column=0, sticky='w', pady=(5, 2))
        
        currency_var = tk.StringVar(value="USD")
        currency_menu = ttk.Combobox(form,
                                     textvariable=currency_var,
                                     values=['USD', 'EUR', 'GBP', 'JPY'],
                                     font=self.FONTS['body'],
                                     state='readonly')
        currency_menu.grid(row=2, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        form.grid_columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def create_account():
            try:
                account_type = account_type_var.get()
                initial_balance = float(balance_var.get())
                currency = currency_var.get()
                
                if initial_balance < 0:
                    messagebox.showerror("Error", "Initial balance cannot be negative")
                    return
                
                account = self.service.create_account(
                    customer_id=self.current_customer_id,
                    account_type=account_type,
                    initial_balance=initial_balance
                )
                
                self._load_customer_accounts()
                self._update_stats()
                dialog.destroy()
                messagebox.showinfo("Success", f"Created {account_type} account: {account.account_number}")
                self._set_status(f"Created account: {account.account_number}")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create account: {e}")
        
        tk.Button(btn_frame,
                 text="🏦 Create Account",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['success'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=create_account).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    # ========================================================================
    # Transaction Operations
    # ========================================================================
    
    def _deposit(self):
        """Deposit money"""
        self._show_transaction_dialog("Deposit", "💰", self.COLORS['success'])
    
    def _withdraw(self):
        """Withdraw money"""
        self._show_transaction_dialog("Withdraw", "💸", self.COLORS['warning'])
    
    def _show_transaction_dialog(self, operation, icon, color):
        """Show transaction dialog"""
        if not self.current_account_id:
            messagebox.showwarning("Warning", "Please select an account first")
            return
        
        account = self.service.get_account(self.current_account_id)
        if not account:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{operation} Money")
        dialog.geometry("400x300")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        tk.Label(dialog,
                text=f"{icon} {operation} Money",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=color).pack(pady=20)
        
        tk.Label(dialog,
                text=f"Account: {account.account_number} ({account.account_type})",
                font=self.FONTS['body'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack()
        
        tk.Label(dialog,
                text=f"Balance: ${account.balance:,.2f}",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(pady=5)
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(form,
                text="Amount:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(form,
                               textvariable=amount_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        amount_entry.grid(row=0, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        amount_entry.focus()
        
        tk.Label(form,
                text="Description:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        desc_var = tk.StringVar(value=operation)
        desc_entry = tk.Entry(form,
                             textvariable=desc_var,
                             font=self.FONTS['body'],
                             bg=self.COLORS['light'],
                             relief='flat',
                             bd=0,
                             highlightthickness=1,
                             highlightcolor=self.COLORS['primary'])
        desc_entry.grid(row=1, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        form.grid_columnconfigure(1, weight=1)
        
        def process_transaction():
            try:
                amount = float(amount_var.get())
                description = desc_var.get().strip() or operation
                
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                
                if operation == "Deposit":
                    self.service.deposit(self.current_account_id, amount, description)
                else:
                    self.service.withdraw(self.current_account_id, amount, description)
                
                self._load_customer_accounts()
                self._load_transactions(self.current_account_id)
                self._update_stats()
                dialog.destroy()
                messagebox.showinfo("Success", f"{operation} of ${amount:,.2f} completed")
                self._set_status(f"{operation} of ${amount:,.2f} completed")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to {operation.lower()}: {e}")
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Button(btn_frame,
                 text=f"✅ {operation}",
                 font=self.FONTS['body_bold'],
                 bg=color,
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=process_transaction).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    def _transfer(self):
        """Transfer money between accounts"""
        if not self.current_account_id:
            messagebox.showwarning("Warning", "Please select an account first")
            return
        
        account = self.service.get_account(self.current_account_id)
        if not account:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Transfer Money")
        dialog.geometry("450x350")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"450x350+{x}+{y}")
        
        tk.Label(dialog,
                text="🔄 Transfer Money",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['info']).pack(pady=20)
        
        tk.Label(dialog,
                text=f"From: {account.account_number} (Balance: ${account.balance:,.2f})",
                font=self.FONTS['body'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack()
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(form,
                text="To Account Number:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        to_account_var = tk.StringVar()
        to_account_entry = tk.Entry(form,
                                   textvariable=to_account_var,
                                   font=self.FONTS['body'],
                                   bg=self.COLORS['light'],
                                   relief='flat',
                                   bd=0,
                                   highlightthickness=1,
                                   highlightcolor=self.COLORS['primary'])
        to_account_entry.grid(row=0, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        tk.Label(form,
                text="Amount:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(form,
                               textvariable=amount_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        amount_entry.grid(row=1, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        amount_entry.focus()
        
        tk.Label(form,
                text="Description:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=2, column=0, sticky='w', pady=(5, 2))
        
        desc_var = tk.StringVar(value="Transfer")
        desc_entry = tk.Entry(form,
                             textvariable=desc_var,
                             font=self.FONTS['body'],
                             bg=self.COLORS['light'],
                             relief='flat',
                             bd=0,
                             highlightthickness=1,
                             highlightcolor=self.COLORS['primary'])
        desc_entry.grid(row=2, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        form.grid_columnconfigure(1, weight=1)
        
        def process_transfer():
            try:
                to_account_number = to_account_var.get().strip()
                amount = float(amount_var.get())
                description = desc_var.get().strip() or "Transfer"
                
                if not to_account_number:
                    messagebox.showerror("Error", "Destination account number is required")
                    return
                
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                
                self.service.transfer(self.current_account_id, to_account_number, amount, description)
                
                self._load_customer_accounts()
                self._load_transactions(self.current_account_id)
                self._update_stats()
                dialog.destroy()
                messagebox.showinfo("Success", f"Transferred ${amount:,.2f} to {to_account_number}")
                self._set_status(f"Transferred ${amount:,.2f} to {to_account_number}")
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to transfer: {e}")
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Button(btn_frame,
                 text="🔄 Transfer",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['info'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=process_transfer).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    # ========================================================================
    # Loan Operations
    # ========================================================================
    
    def _apply_loan(self):
        """Apply for a loan"""
        if not self.current_customer_id:
            messagebox.showwarning("Warning", "Please select a customer first")
            return
        
        customer = self.service.get_customer(self.current_customer_id)
        if not customer:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Apply for Loan")
        dialog.geometry("450x450")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"450x450+{x}+{y}")
        
        tk.Label(dialog,
                text="💰 Apply for Loan",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['warning']).pack(pady=20)
        
        tk.Label(dialog,
                text=f"Customer: {customer.get_full_name()}",
                font=self.FONTS['body'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack()
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30, pady=20)
        
        tk.Label(form,
                text="Loan Type:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        loan_type_var = tk.StringVar(value="Personal")
        loan_type_menu = ttk.Combobox(form,
                                     textvariable=loan_type_var,
                                     values=Loan.LOAN_TYPES,
                                     font=self.FONTS['body'],
                                     state='readonly')
        loan_type_menu.grid(row=0, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        tk.Label(form,
                text="Amount:",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=1, column=0, sticky='w', pady=(5, 2))
        
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(form,
                               textvariable=amount_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        amount_entry.grid(row=1, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        amount_entry.focus()
        
        tk.Label(form,
                text="Term (months):",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=2, column=0, sticky='w', pady=(5, 2))
        
        term_var = tk.StringVar(value="12")
        term_entry = tk.Entry(form,
                             textvariable=term_var,
                             font=self.FONTS['body'],
                             bg=self.COLORS['light'],
                             relief='flat',
                             bd=0,
                             highlightthickness=1,
                             highlightcolor=self.COLORS['primary'])
        term_entry.grid(row=2, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        tk.Label(form,
                text="Interest Rate (%):",
                font=self.FONTS['body_bold'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).grid(row=3, column=0, sticky='w', pady=(5, 2))
        
        rate_var = tk.StringVar(value="8.0")
        rate_entry = tk.Entry(form,
                             textvariable=rate_var,
                             font=self.FONTS['body'],
                             bg=self.COLORS['light'],
                             relief='flat',
                             bd=0,
                             highlightthickness=1,
                             highlightcolor=self.COLORS['primary'])
        rate_entry.grid(row=3, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
        
        form.grid_columnconfigure(1, weight=1)
        
        def submit_loan():
            try:
                loan_type = loan_type_var.get()
                amount = float(amount_var.get())
                term_months = int(term_var.get())
                interest_rate = float(rate_var.get()) / 100
                
                if amount <= 0:
                    messagebox.showerror("Error", "Loan amount must be positive")
                    return
                
                if term_months <= 0:
                    messagebox.showerror("Error", "Term must be positive")
                    return
                
                loan = self.service.apply_for_loan(
                    customer_id=self.current_customer_id,
                    amount=amount,
                    loan_type=loan_type,
                    term_months=term_months,
                    interest_rate=interest_rate
                )
                
                dialog.destroy()
                messagebox.showinfo("Success", 
                                   f"Loan application submitted!\n\n"
                                   f"Amount: ${amount:,.2f}\n"
                                   f"Type: {loan_type}\n"
                                   f"Monthly Payment: ${loan.calculate_monthly_payment():,.2f}\n"
                                   f"Status: {loan.status}")
                self._set_status(f"Loan application submitted: {loan.loan_number}")
                self._load_data()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit loan: {e}")
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Button(btn_frame,
                 text="💰 Submit Application",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['warning'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=submit_loan).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    def _calculate_interest(self):
        """Calculate interest for all accounts"""
        count = self.service.calculate_interest_for_all()
        self._load_data()
        self._set_status(f"Calculated interest for {count} accounts")
        messagebox.showinfo("Interest Calculated", 
                           f"Interest calculated for {count} accounts\n\n"
                           f"Total balance: ${self.service.get_total_balance():,.2f}")
    
    # ========================================================================
    # Refresh and Demo Data
    # ========================================================================
    
    def _refresh_data(self):
        """Refresh all data"""
        self._load_data()
        self._set_status("Data refreshed")
    
    def _create_demo_data(self):
        """Create demo data if none exists"""
        if self.service.get_customer_count() > 0:
            return
        
        # Create demo customers
        demo_customers = [
            ("John", "Doe", "john.doe@email.com", "555-0101", "123 Main St, NY", "1985-03-15"),
            ("Jane", "Smith", "jane.smith@email.com", "555-0102", "456 Oak Ave, LA", "1990-07-22"),
            ("Robert", "Johnson", "robert.j@email.com", "555-0103", "789 Pine Rd, SF", "1978-11-09"),
            ("Emily", "Davis", "emily.davis@email.com", "555-0104", "321 Elm St, CHI", "1995-02-18"),
            ("Michael", "Brown", "michael.b@email.com", "555-0105", "654 Maple Dr, MIA", "1982-09-30")
        ]
        
        customers = []
        for first, last, email, phone, address, dob in demo_customers:
            try:
                customer = self.service.add_customer(
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone=phone,
                    address=address,
                    date_of_birth=dob
                )
                customers.append(customer)
                
                # Create accounts for each customer
                account_types = ['Savings', 'Checking']
                for acc_type in account_types:
                    initial = random.uniform(1000, 10000)
                    self.service.create_account(customer.id, acc_type, initial)
                
                # Add a loan for some customers
                if random.random() > 0.6:
                    loan_amount = random.uniform(5000, 25000)
                    loan = self.service.apply_for_loan(
                        customer.id,
                        loan_amount,
                        random.choice(['Personal', 'Auto', 'Home']),
                        random.choice([12, 24, 36, 48])
                    )
                    if random.random() > 0.3:
                        self.service.approve_loan(loan.id)
                
            except Exception:
                continue
        
        self._load_data()
        self._set_status(f"Created demo data with {len(customers)} customers")
        self._update_stats()

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = BankSimulatorApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()