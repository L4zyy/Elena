import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

from pathFinder import PathFinder

class MapModel():
    def __init__(self, eps=1e-5, city='Amherst, Massachusetts, USA', network_type='drive', timeout=100):

        self._eps = eps         # parameter for the inverse calculation

        self.pathFinder = PathFinder(timeout)

        # get map data graph for some city
        self.G = ox.graph_from_place(city, network_type=network_type)

    
    def add_elevation_info(self, api_key=None):
        if api_key is None:
            with open("api_key.txt", "r") as f:
                api_key = f.readline()

        self.G = ox.add_node_elevations(self.G, api_key=api_key)
        self.G = ox.add_edge_grades(self.G)

        # calculate inverse grade_abs for maximum elevation path
        for e in self.G.edges:
            self.G.edges[e]['inv_grade_abs'] = 1 / (self.G.edges[e]['grade_abs'] + self._eps)

    def get_path(self, start, end, limit_ratio=1.5, weight='height', inverse=False):
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