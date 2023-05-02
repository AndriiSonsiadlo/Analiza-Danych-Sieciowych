import collections
import functools

import haversine

from Heap import Heap

Airport = collections.namedtuple('Airport', 'code name country latitude longitude')
Flight = collections.namedtuple('Flight', 'origin destination')
Route = collections.namedtuple('Route', 'price path')


class Graph:
    """ A hash-table implementation of an undirected graph."""

    def __init__(self):
        # Map each node to a set of nodes connected to it
        self._neighbors = collections.defaultdict(set)

    def connect(self, node1, node2):
        self._neighbors[node1].add(node2)
        self._neighbors[node2].add(node1)

    def neighbors(self, node):
        yield from self._neighbors[node]

    @classmethod
    def load(cls, flights, airports):
        """Return a populated Graph object with real airports and routes."""

        world = cls()
        for flight in flights:
            try:
                origin = airports[flight.origin]
                destination = airports[flight.destination]
                world.connect(origin, destination)
            # Ignore flights to or from an unknown airport
            except KeyError:
                continue
        return world

    @staticmethod
    @functools.lru_cache()
    def get_price(origin, destination, cents_per_km=0.1):
        """Return the cheapest flight without stops."""

        # Haversine distance, in kilometers
        point1 = origin.latitude, origin.longitude,
        point2 = destination.latitude, destination.longitude
        distance = haversine.haversine(point1, point2)
        return distance * cents_per_km

    def dijkstra(self, origin, destination):
        """Use Dijkstra's algorithm to find the cheapest path."""

        routes = Heap()
        for neighbor in self.neighbors(origin):
            price = self.get_price(origin, neighbor)
            routes.push(Route(price=price, path=[origin, neighbor]))

        visited = set()
        visited.add(origin)

        while routes:

            # Find the nearest yet-to-visit airport
            price, path = routes.pop()
            airport = path[-1]
            if airport in visited:
                continue

            # We have arrived! Wo-hoo!
            if airport is destination:
                return price, path

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(airport):
                if neighbor not in visited:
                    # Total spent so far plus the price of getting there
                    new_price = price + self.get_price(airport, neighbor)
                    new_path = path + [neighbor]
                    routes.push(Route(new_price, new_path))

            visited.add(airport)

        return float('infinity'), None




    def bellman_ford(self, origin, destination):
        """Use Bellman Ford's algorithm to find the cheapest path."""

        routes = []
        for neighbor in self.neighbors(origin):
            price = self.get_price(origin, neighbor)
            routes.append(Route(price=price, path=[origin, neighbor]))

        while routes:
            old_route = routes.pop(0)
            airport = old_route.path[-1]

            for neighbor in self.neighbors(airport):
                new_route = Route(old_route.price + self.get_price(airport, neighbor), path=old_route.path + [neighbor])

                if self.check_same_route(routes, new_route) and destination == new_route.path[-1]:
                    continue
                else:
                    routes.append(new_route)

        if routes:
            return routes[0].price, routes[0].path

        return float('infinity'), None

    def check_same_route(self, routes: list[Route], route2: Route):
        for i, route1 in enumerate(routes):
            if route1.path[0] == route2.path[0] and route1.path[-1] == route2.path[-1]:
                if route1.price > route2.price:
                    routes[i] = route2
                    return True
        else:
            return False

    def bellman_ford2(self, origin, destination):
        # Relax edges repeatedly
        price = 0
        for neighbor in self.neighbors(origin):
            for u, v in self.edges():
                weight = self.get_weight(u, v)
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

        # Check for negative cycles
        for u, v in self.edges():
            weight = self.get_weight(u, v)
            if distances[u] + weight < distances[v]:
                raise ValueError("Negative cycle detected")

        # Build path to destination
        path = []
        node = destination
        while node is not None:
            path.append(node)
            node = predecessors[node]
        path.reverse()

        return distances[destination], path

    def bellman_ford3(self, origin, destination):
        """Use the Bellman-Ford algorithm to find the cheapest path."""

        distances = {airport: float('inf') for airport in self._neighbors}
        distances[origin] = 0

        # Iterate over all the edges in the graph
        for airport in self._neighbors:
            for neighbor in self.neighbors(airport):
                price = self.get_price(airport, neighbor)
                # Update the distance to the neighbor
                if distances[airport] + price < distances[neighbor]:
                    distances[neighbor] = distances[airport] + price

        # Check for negative weight cycles
        for airport in self._neighbors:
            for neighbor in self.neighbors(airport):
                price = self.get_price(airport, neighbor)
                if distances[airport] + price < distances[neighbor]:
                    raise ValueError("Negative weight cycle detected")

        # Build the path from the origin to the destination
        path = [destination]
        while path[-1] != origin:
            for neighbor in self.neighbors(path[-1]):
                if distances[neighbor] + self.get_price(path[-1], neighbor) == distances[path[-1]]:
                    path.append(neighbor)
                    break

        # Reverse the path and return the result
        path.reverse()
        return distances[destination], path