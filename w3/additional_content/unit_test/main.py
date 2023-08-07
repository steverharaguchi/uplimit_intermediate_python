from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


client = TestClient(app)