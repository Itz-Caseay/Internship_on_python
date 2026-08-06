# API.py - Complete Working Code
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uvicorn

# ----- CREATE FASTAPI APP -----
app = FastAPI(
    title="My First API",
    description="A modern, production-ready API built with FastAPI",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your@email.com",
    },
    license_info={
        "name": "MIT License",
    }
)

# ----- DATA MODELS (Pydantic Schemas) -----
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    age: Optional[int] = Field(None, ge=1, le=150, example=30)

class UserResponse(BaseModel):
    """Schema for returning user data"""
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime

class UserUpdate(BaseModel):
    """Schema for updating a user"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=1, le=150)

# ----- IN-MEMORY DATABASE -----
users_db = {}
user_id_counter = 1

# ==============================================
# BEAUTIFUL HOMEPAGE - HTML
# ==============================================
@app.get("/", response_class=HTMLResponse)
async def beautiful_homepage():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My First API</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: #0f0e17;
                padding: 20px;
                position: relative;
                overflow-x: hidden;
            }

            /* Animated Background */
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 50% 100%, rgba(102, 126, 234, 0.05) 0%, transparent 50%);
                z-index: 0;
            }

            /* Floating Orbs */
            .orb {
                position: fixed;
                border-radius: 50%;
                filter: blur(80px);
                opacity: 0.3;
                z-index: 0;
                animation: float 8s ease-in-out infinite;
            }

            .orb-1 {
                width: 300px;
                height: 300px;
                background: #667eea;
                top: -100px;
                left: -100px;
                animation-delay: 0s;
            }

            .orb-2 {
                width: 400px;
                height: 400px;
                background: #764ba2;
                bottom: -150px;
                right: -150px;
                animation-delay: 2s;
            }

            .orb-3 {
                width: 200px;
                height: 200px;
                background: #f093fb;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                animation-delay: 4s;
            }

            @keyframes float {
                0%, 100% { transform: translate(0, 0) scale(1); }
                33% { transform: translate(30px, -30px) scale(1.1); }
                66% { transform: translate(-20px, 20px) scale(0.9); }
            }

            /* Main Container */
            .container {
                position: relative;
                z-index: 1;
                background: rgba(26, 26, 46, 0.8);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 32px;
                padding: 60px;
                max-width: 900px;
                width: 100%;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                animation: slideUp 0.8s ease-out;
            }

            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* Header */
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 40px;
                flex-wrap: wrap;
                gap: 20px;
            }

            .logo-section {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .logo-icon {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2em;
                animation: rotate 10s linear infinite;
            }

            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .logo-text h1 {
                color: white;
                font-size: 2.2em;
                font-weight: 900;
                letter-spacing: -0.5px;
            }

            .logo-text h1 span {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .logo-text .subtitle {
                color: #a7a9be;
                font-size: 0.9em;
                font-weight: 400;
            }

            .badge-container {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }

            .badge {
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.75em;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .badge-primary {
                background: rgba(102, 126, 234, 0.2);
                color: #667eea;
                border: 1px solid rgba(102, 126, 234, 0.2);
            }

            .badge-success {
                background: rgba(76, 175, 80, 0.2);
                color: #4caf50;
                border: 1px solid rgba(76, 175, 80, 0.2);
            }

            /* Hero Section */
            .hero {
                text-align: center;
                padding: 20px 0 30px;
            }

            .hero h2 {
                color: white;
                font-size: 2.8em;
                font-weight: 800;
                margin-bottom: 15px;
                line-height: 1.2;
            }

            .hero h2 .highlight {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .hero p {
                color: #a7a9be;
                font-size: 1.2em;
                max-width: 600px;
                margin: 0 auto;
                line-height: 1.6;
            }

            /* Stats Grid */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }

            .stat-card {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 25px;
                text-align: center;
                transition: all 0.3s ease;
                cursor: default;
            }

            .stat-card:hover {
                transform: translateY(-5px);
                border-color: rgba(102, 126, 234, 0.3);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.1);
            }

            .stat-icon {
                font-size: 2em;
                display: block;
                margin-bottom: 10px;
            }

            .stat-number {
                font-size: 2.5em;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1;
            }

            .stat-label {
                color: #a7a9be;
                font-size: 0.9em;
                margin-top: 8px;
                font-weight: 400;
            }

            /* Quick Links */
            .quick-links {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 15px;
                margin: 30px 0;
            }

            .quick-link {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 20px 25px;
                text-decoration: none;
                color: white;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 18px;
                position: relative;
                overflow: hidden;
            }

            .quick-link::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .quick-link:hover::before {
                opacity: 1;
            }

            .quick-link:hover {
                transform: translateX(5px);
                border-color: rgba(102, 126, 234, 0.3);
            }

            .quick-link .icon {
                font-size: 1.8em;
                width: 50px;
                height: 50px;
                background: rgba(102, 126, 234, 0.15);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                position: relative;
                z-index: 1;
            }

            .quick-link .info {
                position: relative;
                z-index: 1;
                flex: 1;
            }

            .quick-link .info h3 {
                font-size: 1em;
                font-weight: 600;
                margin-bottom: 3px;
            }

            .quick-link .info p {
                color: #a7a9be;
                font-size: 0.85em;
            }

            .quick-link .arrow {
                color: #667eea;
                font-size: 1.5em;
                position: relative;
                z-index: 1;
                transition: transform 0.3s ease;
            }

            .quick-link:hover .arrow {
                transform: translateX(5px);
            }

            /* Status Bar */
            .status-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 30px;
                padding-top: 30px;
                border-top: 1px solid rgba(255, 255, 255, 0.05);
                flex-wrap: wrap;
                gap: 15px;
            }

            .status-indicator {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .status-dot {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #4caf50;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(0.8); }
            }

            .status-text {
                color: #a7a9be;
                font-size: 0.9em;
            }

            .status-text strong {
                color: white;
                font-weight: 600;
            }

            .footer-text {
                color: #444;
                font-size: 0.85em;
            }

            .footer-text a {
                color: #667eea;
                text-decoration: none;
                transition: color 0.3s ease;
            }

            .footer-text a:hover {
                color: #764ba2;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 30px 20px;
                }
                
                .hero h2 {
                    font-size: 2em;
                }
                
                .logo-text h1 {
                    font-size: 1.6em;
                }
                
                .stats-grid {
                    grid-template-columns: repeat(2, 1fr);
                    gap: 12px;
                }
                
                .quick-links {
                    grid-template-columns: 1fr;
                }
                
                .header {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .status-bar {
                    flex-direction: column;
                    align-items: flex-start;
                }
            }

            @media (max-width: 480px) {
                .stats-grid {
                    grid-template-columns: 1fr 1fr;
                }
                
                .stat-number {
                    font-size: 1.8em;
                }
                
                .hero h2 {
                    font-size: 1.6em;
                }
            }
        </style>
    </head>
    <body>
        <!-- Floating Orbs -->
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>

        <!-- Main Container -->
        <div class="container">
            <!-- Header -->
            <div class="header">
                <div class="logo-section">
                    <div class="logo-icon">🚀</div>
                    <div class="logo-text">
                        <h1>My<span>API</span></h1>
                        <div class="subtitle">FastAPI Backend</div>
                    </div>
                </div>
                <div class="badge-container">
                    <span class="badge badge-primary">v1.0.0</span>
                    <span class="badge badge-success">● Live</span>
                </div>
            </div>

            <!-- Hero -->
            <div class="hero">
                <h2>
                    Build Something <span class="highlight">Amazing</span>
                </h2>
                <p>
                    Your API is ready to handle requests. Explore the documentation 
                    and start building your application today.
                </p>
            </div>

            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-icon">📊</span>
                    <div class="stat-number">5</div>
                    <div class="stat-label">Endpoints</div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">👥</span>
                    <div class="stat-number">0</div>
                    <div class="stat-label">Users</div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">🟢</span>
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Uptime</div>
                </div>
                <div class="stat-card">
                    <span class="stat-icon">⏱️</span>
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Available</div>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="quick-links">
                <a href="/docs" class="quick-link">
                    <div class="icon">📚</div>
                    <div class="info">
                        <h3>Swagger UI</h3>
                        <p>Interactive API documentation</p>
                    </div>
                    <span class="arrow">→</span>
                </a>
                <a href="/redoc" class="quick-link">
                    <div class="icon">📖</div>
                    <div class="info">
                        <h3>ReDoc</h3>
                        <p>Beautiful API reference</p>
                    </div>
                    <span class="arrow">→</span>
                </a>
                <a href="/health" class="quick-link">
                    <div class="icon">❤️</div>
                    <div class="info">
                        <h3>Health Check</h3>
                        <p>Monitor API status</p>
                    </div>
                    <span class="arrow">→</span>
                </a>
            </div>

            <!-- Status Bar -->
            <div class="status-bar">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span class="status-text">
                        <strong>All Systems Operational</strong> · Ready to serve requests
                    </span>
                </div>
                <div class="footer-text">
                    Made with ❤️ using <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a> · Python
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# ==============================================
# API ENDPOINTS
# ==============================================

# ----- HEALTH CHECK -----
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API status
    """
    return {
        "status": "healthy",
        "users_count": len(users_db),
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ----- GET ALL USERS -----
@app.get("/api/users", response_model=List[UserResponse], tags=["Users"])
async def get_users():
    """
    Retrieve all users from the database
    """
    return list(users_db.values())

# ----- GET SINGLE USER -----
@app.get("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: int):
    """
    Retrieve a specific user by ID
    """
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user

# ----- CREATE USER -----
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """
    Create a new user
    
    - **name**: User's full name (required)
    - **email**: Valid email address (required)
    - **age**: User's age (optional, must be between 1 and 150)
    """
    global user_id_counter
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now()
    }
    
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user

# ----- UPDATE USER -----
@app.put("/api/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(user_id: int, user: UserUpdate):
    """
    Update an existing user
    
    All fields are optional. Only provided fields will be updated.
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if email is taken by another user
    if user.email:
        for existing_user in users_db.values():
            if existing_user["email"] == user.email and existing_user["id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered by another user"
                )
    
    # Update only provided fields
    if user.name is not None:
        users_db[user_id]["name"] = user.name
    if user.email is not None:
        users_db[user_id]["email"] = user.email
    if user.age is not None:
        users_db[user_id]["age"] = user.age
    
    return users_db[user_id]

# ----- DELETE USER -----
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user by ID
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    del users_db[user_id]
    return None

# ==============================================
# RUN THE APPLICATION
# ==============================================
if __name__ == "__main__":
    uvicorn.run(
        "API:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )