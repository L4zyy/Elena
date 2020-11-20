import unittest
from mapModel import MapModel

class TestMapModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.model = MapModel()

        with open('api_key.txt', 'r') as f:
            key = f.readline()
        self.model.add_elevation_info(key)

        self.orig = (42.3756519, -72.51983)
        self.dest = (42.3993014, -72.5106863)

    def test_weight_sum(self):
        path, coords, path_length, path_elevation_gain, sp_len, sp_grad = self.model.get_path(self.orig, self.dest)

        self.assertEquals(sp_len, 3031)
        self.assertEquals(sp_grad, 58)
        self.assertEquals(path_length, 3366)
        self.assertEquals(path_elevation_gain, 57)
    
    def test_path_finer_functionality(self):
        path, coords, path_length, path_elevation_gain, sp_len, sp_grad = self.model.get_path(self.orig, self.dest, limit_ratio=1.0, weight='height')
        self.assertEquals((path_length, path_elevation_gain), (sp_len, sp_grad))

        path, coords, path_length, path_elevation_gain, sp_len, sp_grad = self.model.get_path(self.orig, self.dest, limit_ratio=1.5, weight='height', inverse=False)
        self.assertGreater(path_length, sp_len)
        self.assertLess(path_elevation_gain, sp_grad)

        path, coords, path_length, path_elevation_gain, sp_len, sp_grad = self.model.get_path(self.orig, self.dest, limit_ratio=1.5, weight='height', inverse=True)
        self.assertGreater(path_length, sp_len)
        self.assertGreater(path_elevation_gain, sp_grad)

if __name__ == '__main__':
    unittest.main()