import uuid
from datetime import datetime
import bcrypt
from typing import List, Optional

class User:
    """User model representing a bank customer"""
    
    def __init__(self, username: str, email: str, password: str, full_name: str):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self._password = None  # Store hashed password
        self.full_name = full_name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_active = True
        self.account_ids = []  # List of account IDs
        
        # Hash the password
        self.set_password(password)
    
    def set_password(self, password: str) -> None:
        """Hash and set the password"""
        salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        if not self._password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self._password)
    
    def add_account(self, account_id: str) -> None:
        """Add an account to the user"""
        if account_id not in self.account_ids:
            self.account_ids.append(account_id)
            self.updated_at = datetime.now()
    
    def update_profile(self, full_name: Optional[str] = None, email: Optional[str] = None) -> None:
        """Update user profile"""
        if full_name:
            self.full_name = full_name
        if email:
            self.email = email
        self.updated_at = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False
        self.updated_at = datetime.now()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active,
            'accounts': self.account_ids
        }
        
        if include_sensitive:
            data['password_hash'] = self._password.decode('utf-8') if self._password else None
        
        return data
    
    def __repr__(self):
        return f"<User {self.username} ({self.id})>"