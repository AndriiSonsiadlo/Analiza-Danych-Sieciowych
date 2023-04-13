import csv

from Graph import Graph, Airport, Flight


def get_airports(path='airports.dat'):
    """Return a generator that yields Airport objects."""

    with open(path, 'rt', encoding="utf8") as fd:
        reader = csv.reader(fd)
        for row in reader:
            name = row[1]
            country = row[3]
            code = row[4]  # IATA code (eg, 'BCN' for Barcelona)
            latitude = float(row[6])  # Decimal degrees; negative is South.
            longitude = float(row[7])  # Decimal degrees; negative is West.
            yield Airport(code, name, country, latitude, longitude)


def get_flights(path='flights.dat'):
    """Return a generator that yields direct Flight objects."""

    with open(path, 'rt', encoding="utf8") as fd:
        reader = csv.reader(fd)
        for row in reader:
            origin = row[2]  # IATA code of source ...
            destination = row[4]  # ... and destination airport.
            nstops = int(row[7])  # Number of stops; zero for direct.
            if not nstops:
                yield Flight(origin, destination)


# Make it possible to easily look up airports by IATA code.
AIRPORTS = {airport.code: airport for airport in get_airports()}
FLIGHTS = [flight for flight in get_flights()]

if __name__ == "__main__":
    world = Graph.load(FLIGHTS, AIRPORTS)
    valencia = AIRPORTS['HGU']
    portland = AIRPORTS['CPO']
    print(type(valencia), "\n", type(portland))
    distance, path = world.dijkstra(valencia, portland)

    if path is not None:
        for index, airport in enumerate(path):
            print(index, '|', airport)
    print(distance, '€')
