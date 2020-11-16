import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
#%matplotlib inline
ox.config(use_cache=True, log_console=True)
ox.__version__


def get_path(start_coord, end_coord, func=None):
    if func == None:
        func = nx.astar_path
    
    orig = ox.get_nearest_node(G, start_coord)
    dest = ox.get_nearest_node(G, end_coord)
    route = func(G, orig, dest, weight='length')
    coords = []
    for node in route:
        coords.append((G.nodes[node]['x'], G.nodes[node]['y']))
    
    return route, coords


# get a graph for some city
G = ox.graph_from_place('Amherst, Massachusetts, USA', network_type='drive')
#fig, ax = ox.plot_graph(G)


# add elevation to nodes automatically, calculate edge grades, plot network
# you need a google elevation api key to run this cell!

from key import google_elevation_api_key
G = ox.add_node_elevations(G, api_key=google_elevation_api_key)
G = ox.add_edge_grades(G)
nc = ox.plot.get_node_colors_by_attr(G, 'elevation', cmap='plasma')
#fig, ax = ox.plot_graph(G, node_color=nc, node_size=20, edge_linewidth=2, edge_color='#333')

# impute missing edge speeds then calculate edge travel times
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

start_coord = (42.3756519, -72.51983)
end_coord = (42.3993014, -72.5106863)
route, coords = get_path(start_coord, end_coord)
print(coords)
#fig, ax = ox.plot_graph_route(G, route, node_size=0)

print("length: ", sum(ox.utils_graph.get_route_edge_attributes(G, route, 'length')))
print("grade abs: ", sum(ox.utils_graph.get_route_edge_attributes(G, route, 'grade_abs')))