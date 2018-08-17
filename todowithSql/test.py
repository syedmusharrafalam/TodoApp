import unittest
import os
import sys, json
from app import app

class TodoData(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
 
        self.assertEquals(app.debug, False)

    def tearDown(self):
        pass
    
    def test_todo_api(self):
        response = self.app.get('/task/musharraf/api/v1.0/todoapp')
        self.assertEqual(response.status_code,200 )
if __name__ == "__main__":
        unittest.main() 
