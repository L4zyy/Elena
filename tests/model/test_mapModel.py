import unittest
from mapModel import MapModel

class TestMapModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.model = MapModel()

        with open('api_key.txt', 'r') as f:
            key = f.readline()
        self.model.add_elevation_info(key)

    def test_minmax(self):
        
        self.assertNotEqual(self.model.min_x, float('inf'))
        self.assertNotEqual(self.model.max_x, -float('inf'))
        self.assertNotEqual(self.model.min_y, float('inf'))
        self.assertNotEqual(self.model.max_y, -float('inf'))
    
    def test_elevation_info(self):
        node_id = list(self.model.G.nodes)[0]
        edge_id = list(self.model.G.edges)[0]
        node_info = self.model.G.nodes[node_id]
        edge_info = dict(self.model.G[edge_id[0]][edge_id[1]][0])

        self.assertTrue('elevation' in node_info)
        self.assertTrue('grade' in edge_info)

if __name__ == '__main__':
    unittest.main()