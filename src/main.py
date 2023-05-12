from Graph import Graph
from utils import get_flights, get_airports

# Make it possible to easily look up airports by IATA code.
AIRPORTS = {airport.code: airport for airport in get_airports()}
FLIGHTS = [flight for flight in get_flights()]


def display_result(distance, path, number_of_checks):
    print(f"{'Number of airport checks: '}{number_of_checks:>4}")
    if path is not None:
        for index, airport in enumerate(path, start=1):
            print(index, '|', airport)
    print(round(Graph.get_price(distance), 2), '€', end="\n\n")


if __name__ == "__main__":
    world = Graph.load(FLIGHTS, AIRPORTS)

    print(f"{'Path from Papua New Guinea to Angola':^150}")
    papua_new_guinea = AIRPORTS['IAA']
    angola = AIRPORTS['BSB']
    display_result(*world.dijkstra(papua_new_guinea, angola))
    display_result(*world.a_star(papua_new_guinea, angola))

    # print(f"{'Path from Valencia to Portland':^150}")
    # valencia = AIRPORTS['VLC']
    # portland = AIRPORTS['PDX']
    # display_result(*world.dijkstra(valencia, portland))
    # display_result(*world.a_star(valencia, portland))
