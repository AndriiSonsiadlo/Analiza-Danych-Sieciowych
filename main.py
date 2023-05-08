from Graph import Graph
from utils import get_flights, get_airports

# Make it possible to easily look up airports by IATA code.
AIRPORTS = {airport.code: airport for airport in get_airports()}
FLIGHTS = [flight for flight in get_flights()]


def display_result(distance, path, title=""):
    print(f"{' ' + title + ' algorithm ':-^40}")
    if path is not None:
        for index, airport in enumerate(path):
            print(index, '|', airport)
    print(distance, '€', end="\n\n")


if __name__ == "__main__":
    world = Graph.load(FLIGHTS, AIRPORTS)

    print(f"{'Path from Papua New Guinea to Angola':^150}")
    papua_new_guinea = AIRPORTS['HGU']
    angola = AIRPORTS['NBC']
    display_result(*world.dijkstra(papua_new_guinea, angola), title="Dijkstra")
    display_result(*world.a_star(papua_new_guinea, angola), title="A*")

    print(f"{'Path from Valencia to Portland':^150}")
    valencia = AIRPORTS['VLC']
    portland = AIRPORTS['PDX']
    display_result(*world.dijkstra(valencia, portland), title="Dijkstra")
    display_result(*world.a_star(valencia, portland), title="A*")
