# API.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="My First API",
    description="Learning to build APIs with Python",
    version="1.0.0"
)

# ----- DATA MODELS -----
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int]
    created_at: datetime

# ----- In-memory database -----
users_db = {}
user_id_counter = 1

# ----- ROOT ENDPOINT -----
@app.get("/")
async def root():
    return {
        "message": "Welcome to my API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# ----- GET all users -----
@app.get("/api/users", response_model=List[UserResponse])
async def get_users():
    return list(users_db.values())

# ----- GET single user -----
@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user

# ----- POST create user -----
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
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

# ----- PUT update user -----
@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Check if email is taken by another user
    for existing_user in users_db.values():
        if existing_user["email"] == user.email and existing_user["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user"
            )
    
    users_db[user_id].update({
        "name": user.name,
        "email": user.email,
        "age": user.age
    })
    return users_db[user_id]

# ----- DELETE user -----
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    del users_db[user_id]
    return None  # 204 No Content

# ----- HEALTH CHECK -----
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "users_count": len(users_db),
        "timestamp": datetime.now().isoformat()
    }

# ----- RUN THE APP -----
if __name__ == "__main__":
    uvicorn.run(
        "API:app",  # filename:app_instance
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )