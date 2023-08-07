from fastapi.testclient import TestClient
from main import app
import unittest

client = TestClient(app)


class TestApp(unittest.TestCase):
    def test_read_item(self):
        response = client.get("/items/42")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"item_id": 42, "q": None})

    def test_read_item_fail(self):
        response = client.get("/items/42")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"item_id": 52, "q": None})

    def test_read_item_with_query_param(self):
        response = client.get("/items/42?q=test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"item_id": 42, "q": "test"})

    def test_read_item_with_query_param_fail(self):
        response = client.get("/items/42?q=test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"item_id": 52, "q": "test"})
