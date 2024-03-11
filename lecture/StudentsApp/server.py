from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

# Define data models
class Classroom(BaseModel):
    name: str
    difficulty: int

class Student(BaseModel):
    full_name: str
    classes: Optional[List[Classroom]] = []


# Will store the data in-memory
# In real-life it's gonna be a database
classrooms = []
students = []


# Init FastAPI application
app = FastAPI()


# Implement API routes
@app.get("/")
async def index():
    return {"message": "Welcome to our classes!"}

@app.get("/classrooms")
def get_classrooms():
    return classrooms

@app.get("/students")
def get_students():
    return students


# Adding new classes and students
@app.post("/classrooms")
async def add_classroom(classroom: Classroom):
    classrooms.append(classroom.dict())
    return {
        "message": "New class was added",
        "class": classroom.name
    }

@app.post("/students")
async def add_student(student: Student):
    students.append(student.dict())
    return {
        "message": "New student was added",
        "student_name": student.full_name
    }
