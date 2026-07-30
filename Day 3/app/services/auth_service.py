import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import os
from ..models.user import User

class AuthService:
    """Authentication service handling user registration, login, and token management"""
    
    def __init__(self):
        self.users = {}  # user_id -> User object
        self.refresh_tokens = set()
        self.jwt_secret = os.getenv('JWT_SECRET', '5ca04f9d68b7e1f91d368185d76d6c25fc548da761b29507fb03fae622971e64')
        self.jwt_refresh_secret = os.getenv('JWT_REFRESH_SECRET', '0a7955265abc373d2a40cab9cad88c8c65050ea0cb7f48f5a3b7f4cd4147077b')
    
    def register(self, username: str, email: str, password: str, full_name: str) -> User:
        """Register a new user"""
        # Check if user already exists
        for user in self.users.values():
            if user.username == username:
                raise ValueError("Username already taken")
            if user.email == email:
                raise ValueError("Email already registered")
        
        # Create new user
        user = User(username, email, password, full_name)
        self.users[user.id] = user
        return user
    
    def login(self, username: str, password: str) -> Tuple[User, str, str]:
        """Login user and generate tokens"""
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        if not user.verify_password(password):
            raise ValueError("Invalid credentials")
        
        # Generate tokens
        access_token = self._generate_access_token(user)
        refresh_token = self._generate_refresh_token(user)
        
        self.refresh_tokens.add(refresh_token)
        
        return user, access_token, refresh_token
    
    def _generate_access_token(self, user: User) -> str:
        """Generate access token"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def _generate_refresh_token(self, user: User) -> str:
        """Generate refresh token"""
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, self.jwt_refresh_secret, algorithm='HS256')
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Refresh access token using refresh token"""
        if refresh_token not in self.refresh_tokens:
            raise ValueError("Invalid refresh token")
        
        try:
            payload = jwt.decode(refresh_token, self.jwt_refresh_secret, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = self.users.get(user_id)
            
            if not user:
                raise ValueError("User not found")
            
            return self._generate_access_token(user)
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")
    
    def logout(self, refresh_token: str) -> None:
        """Logout user by removing refresh token"""
        self.refresh_tokens.discard(refresh_token)
    
    def get_user(self, user_id: str) -> User:
        """Get user by ID"""
        user = self.users.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    
    def update_user(self, user_id: str, full_name: Optional[str] = None, email: Optional[str] = None) -> User:
        """Update user profile"""
        user = self.get_user(user_id)
        user.update_profile(full_name, email)
        return user
    
    def deactivate_user(self, user_id: str) -> User:
        """Deactivate user"""
        user = self.get_user(user_id)
        user.deactivate()
        return user