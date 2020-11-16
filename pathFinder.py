import osmnx as ox
import numpy as np

class PathFinder():
    def __init__(self, timeout=100):
        self._timeout = timeout     # timeout limit for finding function

    def get_weight_sum(self, G, route, weight):
        return sum(ox.utils_graph.get_route_edge_attributes(G, route, weight))

    def get_path(self, G, start, end, limit_ratio, weight='length', inverse=False):
        # transfer node coordinates to node ids
        if type(start) is not np.int64:
            start = ox.get_nearest_node(G, start)
            end = ox.get_nearest_node(G, end)

        # calculate shortest path
        sp = ox.shortest_path(G, start, end, weight='length')
        sp_len = get_weight_sum(G, sp, 'length')
        sp_grad = get_weight_sum(G, sp, 'grade_abs')

        print('shortest path: ')
        print("  length: ", sp_len)
        print("  height: ", sp_grad)

        path = None
        if weight is 'length' and inverse is False:
            path = sp
        else:
            if weight is 'height':
                weight = 'grade_abs' if not inverse else 'inv_grade_abs'
            
            path_gen = ox.k_shortest_paths(G, start, end, self.timeout, weight=weight)

            cnt = 0
            for pth in paths:
                cnt += 1
                if get_weight_sum(G, pth, 'length') > limit_ratio * sp_len:
                    continue
                path = pth
                print(cnt)
                print('find path under constraint:')
                print("  length: ", get_weight_sum(G, path, 'length'))
                print("  height: ", get_weight_sum(G, path, 'grade_abs'))
                break

        coords = []
        for node in path:
            coords.append((G.nodes[node]['x'], G.nodes[node]['y']))

        return path, coords