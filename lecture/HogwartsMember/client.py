from pydantic import BaseModel
from typing import Optional

import requests

# Run the FastAPI application before executing the following code
base_url = "http://127.0.0.1:8000"

class HogwartsMember(BaseModel):
    name: str
    house: Optional[str] = None
    year: Optional[int] = None

new_member = HogwartsMember(name="Draco Malfoy", house="Slytherin", year=5)

response = requests.post(f"{base_url}/hogwarts/members", json=new_member.dict())
print(response.json())  # Should print: {'success': True, 'member_id': <new_member_id>}

# http://127.0.0.1:8000/hogwarts/members/2