from fastapi.testclient import TestClient
from server import app, Classroom, Student

# pytest tests.py

client = TestClient(app)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to our classes!"}

def test_create_classroom():
    new_class = Classroom(name="Intermediate Python", difficulty=3)
    response = client.post("/classrooms", json=new_class.dict())
    assert response.status_code == 200
    assert response.json() == {
        "message": "New class was added",
        "class": new_class.name
    }

def test_get_classrooms():
    response = client.get("/classrooms")
    assert response.status_code == 200
    assert response.json() == [Classroom(name="Intermediate Python", difficulty=3).dict()]
