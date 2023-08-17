from w2.utils.database import DB
from w2.utils.response_model import ProcessStatus
import uuid
from datetime import datetime
import time
from pprint import pprint

from fastapi.testclient import TestClient
from w2.server import app
import unittest


class TestApp(unittest.TestCase):
    client = TestClient(app)
    db = DB('db_test.sqlite')

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200, msg='Response code should be 200')
        self.assertEqual(response.json(), {"status": "ok"}, msg='Health API check failed')

    def test_processes(self):
        response = self.client.get("/processes")
        self.assertEqual(response.status_code, 200, msg='Response code should be 200')
        self.assertTrue(isinstance(response.json(), list), msg='Instance of processes object should be list')
        if len(response.json()) > 0:
            self.assertTrue(all([isinstance(process, dict) for process in response.json()]),
                            msg='Process data type should de dictionary')

            response_model_ex = ProcessStatus(process_id='', file_name='', file_path='',
                                              description='', start_time='', end_time='',
                                              percentage=0)

            self.assertTrue(all([process.keys() == response_model_ex.dict().keys()
                                 for process in response.json()]), msg='Missing keys')

    def test_db_operations(self):

        example_data = [{
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_1.csv',
            'file_path': '/usr/sample_1.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_2.csv',
            'file_path': '/usr/sample_2.csv',
            'description': 'sample'
        }, {
            'process_id': str(uuid.uuid4()),
            'start_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'file_name': 'sample_3.csv',
            'file_path': '/usr/sample_3.csv',
            'description': 'sample'
        }]
        for each in example_data:
            self.db.insert(process_id=each['process_id'], start_time=each['start_time'], file_name=each['file_name'],
                           file_path=each['file_path'], description=each['description'])

        time.sleep(5)

        for each in example_data:
            self.db.update_end_time(process_id=each['process_id'],
                                    end_time=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        records = self.db.read_all()
        pprint(records)
