import unittest
import json

import sys 
import os
sys.path.append("../..")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../") for name in dirs])
from app import app

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_empty_input(self):
        # Test Empty form, should throw exception
        ifExcept = False
        try:   
            response = self.client.post("/", data={})
        except:
            ifExcept = True
        self.assertEqual(True,ifExcept)

    def test_correct_input(self):
        # Test valid form, should not throw exception
        ifExcept = False
        try:   
            response = self.client.post("/", data={'slocation':'LatLng(42.38647, -72.53275)','elocation':'LatLng(42.38509, -72.53052)','%distance':'100','minmax':'Min',
                'mapcenter':'LatLng(42.38509, -72.53052)','zoom':'16'})
        except:
            ifExcept = True
        self.assertEqual(False,ifExcept)

    def test_wrong_input_ratioLessThan100(self):
        # Test valid form, should not throw exception
        ifExcept = True
        try:   
            response = self.client.post("/", data={'slocation':'LatLng(42.38647, -72.53275)','elocation':'LatLng(42.38509, -72.53052)','%distance':'20','minmax':'Min',
                'mapcenter':'LatLng(42.38509, -72.53052)','zoom':'16'})
        except:
            ifExcept = False
        self.assertEqual(True,ifExcept)

    def test_wrong_input_inputAllEmpty(self):
        # Test valid form, should not throw exception
        ifExcept = True
        try:   
            response = self.client.post("/", data={'slocation':'','elocation':'','%distance':'','minmax':'',
                'mapcenter':'LatLng(42.38509, -72.53052)','zoom':'16'})
        except:
            ifExcept = False
        self.assertEqual(True,ifExcept)

if __name__ == '__main__':
    unittest.main()