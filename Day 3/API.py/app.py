from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="My API", version="1.0.0")

# ----- DATA MODELS (Pydantic) -----
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

# In-memory database
users_db = {}
user_id_counter = 1

# ----- ENDPOINTS -----
@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}

# GET all users
@app.get("/api/users", response_model=List[UserResponse])
async def get_users():
    return list(users_db.values())

# GET single user
@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# POST create user
@app.post("/api/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global user_id_counter
    
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

# PUT update user
@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db[user_id].update({
        "name": user.name,
        "email": user.email,
        "age": user.age
    })
    return users_db[user_id]

# DELETE user
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted"}

# ----- RUN -----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)