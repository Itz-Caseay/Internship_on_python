from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 1. Initialize the FastAPI Application
app = FastAPI(title="Student Management API")

# 2. Define the Student Data Models using Pydantic
class Student(BaseModel):
    name: str
    age: int
    grade: str

class UpdateStudentModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None

# 3. Simulated Database
students_db = {
    1: {"name": "Alice Smith", "age": 20, "grade": "A"},
    2: {"name": "Bob Jones", "age": 22, "grade": "B"}
}

# --- API ENDPOINTS ---

# GET: Welcome Route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Student API!"}

# GET: Fetch All Students
@app.get("/students")
def get_all_students():
    return students_db

# GET: Fetch a Specific Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student record not found.")
    return students_db[student_id]

# POST: Create a New Student Record
@app.post("/students", status_code=201)
def create_student(student: Student):
    # Auto-increment key strategy
    new_id = max(students_db.keys()) + 1 if students_db else 1
    students_db[new_id] = student.model_dump()
    return {"id": new_id, **students_db[new_id]}

# PUT: Update an Existing Student Record
@app.put("/students/{student_id}")
def update_student(student_id: int, student_data: UpdateStudentModel):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student record not found.")
    
    # Update only the fields provided in the request payload
    current_student = students_db[student_id]
    update_dict = student_data.model_dump(exclude_unset=True)
    
    current_student.update(update_dict)
    return {"id": student_id, **current_student}

# DELETE: Remove a Student Record
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student record not found.")
    
    deleted_student = students_db.pop(student_id)
    return {"message": f"Successfully deleted student: {deleted_student['name']}"}
