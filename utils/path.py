import math


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


class Path:
    def __init__(self, graveyard_id, graveyards_data, coordinates):
        graveyard = next((g for g in graveyards_data if g['id'] == graveyard_id), None)
        self.nodes = graveyard.get("nodes", {})
        self.graph = graveyard.get("graph", {})
        self.sector_coordinates = coordinates
        self.start = graveyard.get('start', [0, 0])
        self.stop = self.closest_node_to_sector()

    def euclidean_heuristic(self, node1, node2):
        x1, y1 = self.nodes[node1]
        x2, y2 = self.nodes[node2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def closest_node_to_sector(self):
        min_distance = float('inf')
        closest_node_coord = None

        for node, node_coord in self.nodes.items():
            node_distance = min(
                distance(node_coord, (self.sector_coordinates[i], self.sector_coordinates[i + 1]))
                for i in range(0, len(self.sector_coordinates), 2)
            )
            if node_distance < min_distance:
                min_distance = node_distance
                closest_node_coord = node_coord

        return closest_node_coord

    def get_neighbors(self, v):
        if v in self.graph:
            return self.graph[v]
        else:
            return None

    def a_star_algorithm(self, destination):
        open_set = set()
        closed_set = set()
        g = {}  # store distance from starting node
        parents = {}  # parents contains an adjacency map of all nodes

        # Find the start_node and stop_node based on coordinates
        start_node = None
        stop_node = None
        for node, coord in self.nodes.items():
            if coord == self.start:
                start_node = node
            elif coord == self.stop:
                stop_node = node

        if start_node is None or stop_node is None:
            print("Start or stop node not found in the provided coordinates.")
            return None

        open_set.add(start_node)
        g[start_node] = 0
        parents[start_node] = start_node

        while len(open_set) > 0:
            n = None

            for v in open_set:
                if n is None or g[v] + self.euclidean_heuristic(v, stop_node) < g[n] + self.euclidean_heuristic(n, stop_node):
                    n = v
            if n == stop_node or self.graph[n] is None:
                pass
            else:
                for (m, weight) in self.get_neighbors(n):
                    if m not in open_set and m not in closed_set:
                        open_set.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n
                            if m in closed_set:
                                closed_set.remove(m)
                                open_set.add(m)

            if n is None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                path = []

                while parents[n] != n:
                    path.append(list(self.nodes[n]))
                    n = parents[n]

                path.append(list(self.nodes[start_node]))

                path.reverse()

                path.append(list(destination))

                print('Path found: {}'.format(path))
                return path

            open_set.remove(n)
            closed_set.add(n)
        print('Path does not exist!')
        return None
