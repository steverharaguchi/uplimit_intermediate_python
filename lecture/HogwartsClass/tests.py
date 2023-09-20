from fastapi.testclient import TestClient
from main import app, HogwartsClass, UpdateClass  # main is your python file

# $pytest tests.py

client = TestClient(app)

def test_hello_world():
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Hogwarts School of Witchcraft and Wizardry"}

def test_create_class():
    new_class = {
        "id": 1,
        "name": "Potions",
        "professor": "Severus Snape",
        "description": "Learn how to brew various magical potions."
    }
    response = client.post("/classes/", json=new_class)
    assert response.status_code == 200
    assert response.json() == {"message": "Class created successfully"}

def test_get_class():
    response = client.get("/classes/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Potions",
        "professor": "Severus Snape",
        "description": "Learn how to brew various magical potions."
    }

def test_update_class():
    updated_class = {
        "id": 1,
        "name": "Potions",
        "professor": "Horace Slughorn",
        "description": "Learn how to brew various magical potions under the guidance of a new professor."
    }
    response = client.put("/classes/1", json=updated_class)
    assert response.status_code == 200
    assert response.json() == {"message": "Class updated successfully"}

def test_partial_update_class():
    partial_update = {
        "name": "Advanced Potions",
        "description": "Learn advanced potion-making techniques."
    }
    response = client.patch("/classes/1", json=partial_update)
    assert response.status_code == 200
    assert response.json() == {"message": "Class partially updated successfully"}

def test_partial_update_class_result():
    response = client.get("/classes/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Advanced Potions",
        "professor": "Horace Slughorn",
        "description": "Learn advanced potion-making techniques."
    }
    
def test_delete_class():
    response = client.delete("/classes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Class deleted successfully"}
