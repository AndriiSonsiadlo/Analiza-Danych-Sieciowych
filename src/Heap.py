import heapq

import haversine

from models import Route, Airport


class Heap:
    """A min-heap."""

    def __init__(self):
        self._values = []

    def push(self, value):
        """Push the value item onto the heap."""
        heapq.heappush(self._values, value)

    def pop(self):
        """ Pop and return the smallest item from the heap."""
        return heapq.heappop(self._values)

    def __len__(self):
        return len(self._values)


class HeuristicHeap:
    """A min-heap."""

    def __init__(self):
        self._values = []

    def get_distance(self, origin: Airport, destination: Airport):
        # Haversine distance, in kilometers
        point1 = origin.latitude, origin.longitude,
        point2 = destination.latitude, destination.longitude
        distance = haversine.haversine(point1, point2)
        return distance

    def push(self, value: Route, destination: Airport):
        """Push the value item onto the heap."""
        heuristic = self.get_distance(value.path[-1], destination)
        priority = value.price + heuristic
        heapq.heappush(self._values, (priority, value))

    def pop(self):
        """ Pop and return the smallest item from the heap."""
        return heapq.heappop(self._values)[1]

    def __len__(self):
        return len(self._values)
