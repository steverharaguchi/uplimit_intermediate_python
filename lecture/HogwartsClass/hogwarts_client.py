import requests

# Run the FastAPI application before executing the following code
base_url = "http://127.0.0.1:8000"

# Example: Create a new Hogwarts class
new_class = {
    "id": 1,
    "name": "Potions",
    "professor": "Severus Snape",
    "description": "Learn how to brew various magical potions."
}

response = requests.post(f"{base_url}/classes/", json=new_class)
print(response.json())

# Example: Update an existing Hogwarts class
updated_class = {
    "id": 1,
    "name": "Potions",
    "professor": "Horace Slughorn",
    "description": "Learn how to brew various magical potions under the guidance of a new professor."
}

response = requests.put(f"{base_url}/classes/1", json=updated_class)
print(response.json())

# Example: Partially update an existing Hogwarts class
partial_update = {
    "name": "Advanced Potions",    
    "description": "Learn advanced potion-making techniques."
}

response = requests.patch(f"{base_url}/classes/1", json=partial_update)
print(response.json())