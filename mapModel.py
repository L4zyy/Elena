import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

from pathFinder import PathFinder

class MapModel():
    def __init__(self, eps=1e-5, city='Amherst, Massachusetts, USA', network_type='drive', timeout=100):
        '''
        Parameters:
            eps (float): epsilon value for the inverse grade calculation
            city (str): city of the map
            network_type (str): type of the map
            timeout (int): timeout for path finding algorithm
        '''

        self._eps = eps         # parameter for the inverse calculation

        self.pathFinder = PathFinder(timeout)

        # get map data graph for some city
        self.G = ox.graph_from_place(city, network_type=network_type)

        self.min_x = float('inf')
        self.max_x = -float('inf')
        self.min_y = float('inf')
        self.max_y = -float('inf')

        for node in self.G.nodes:
            nd = self.G.nodes[node]
            if nd['x'] > self.max_x:
                self.max_x = nd['x']
            if nd['x'] < self.min_x:
                self.min_x = nd['x']
            if nd['y'] > self.max_y:
                self.max_y = nd['y']
            if nd['y'] < self.min_y:
                self.min_y = nd['y']

    
    def add_elevation_info(self, api_key=None):
        '''
        update the elevation and grade information for nodes and edges
        
        Parameters:
            api_key (str): Google API key for the elevation information
        '''
        if api_key is None:
            with open("api_key.txt", "r") as f:
                api_key = f.readline()

        self.G = ox.add_node_elevations(self.G, api_key=api_key)
        self.G = ox.add_edge_grades(self.G)

        for e in self.G.edges:
            # change grade from ratio to value
            self.G.edges[e]['grade_abs'] *= self.G.edges[e]['length']
            # calculate inverse grade_abs for maximum elevation path
            self.G.edges[e]['inv_grade_abs'] = 1 / (self.G.edges[e]['grade_abs'] + self._eps)

    def path_info(self, path):
        '''
        Return the length and elevation gain of the path
        
        Parameters:
            path (int): Path ID
        '''
        length = self.pathFinder.get_weight_sum(self.G, path, 'length')
        height = self.pathFinder.get_weight_sum(self.G, path, 'grade_abs')
        return length, height

    def get_path(self, start, end, limit_ratio=1.5, weight='height', inverse=False):
        '''
        Return the path with certain constraint
        
        Parameters:
            start (float tuple): coordinate for the start point
            end (float tuple): coordinate for the end point
            limit_ratio (float): the length restriction
            weight (str): path type
            inverse (bool): switch between maximum and minimum
        '''
        return self.pathFinder.get_path(self.G, start, end, limit_ratio, weight, inverse)

    def plot_graph(self):
        fig, ax = ox.plot_graph(self.G)
        plt.show()
    
    def plot_path(self, path):
        fig, ax = ox.plot_graph_route(self.G, path, node_size=0)
        plt.show()

if __name__ == "__main__":
    from key import google_elevation_api_key

    timeout = 500
    orig = (42.3926393, -72.5184199)
    dest = (42.3749128, -72.4821135)

    model = MapModel(timeout=timeout)
    model.add_elevation_info(google_elevation_api_key)

    start = ox.get_nearest_node(model.G, orig)
    end = ox.get_nearest_node(model.G, dest)
    limit_ratio = 5

    path, coords = model.pathFinder.get_path(model.G, start, end, limit_ratio, 'height', False)
    print("path", path)
    print("coords", coords)

    model.plot_path(path)