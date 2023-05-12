import csv
import time

from models import Airport, Flight


def get_airports(path='dataset/airports.csv'):
    """Return a generator that yields Airport objects."""

    with open(path, 'rt', encoding="utf8") as fd:
        reader = csv.reader(fd)
        for row in reader:
            name = row[1]
            country = row[3]
            code = row[4]  # IATA code (eg, 'BCN' for Barcelona)
            latitude = float(row[6])  # Decimal degrees; negative is South.
            longitude = float(row[7])  # Decimal degrees; negative is West.
            yield Airport(code=code, name=name, country=country, latitude=latitude, longitude=longitude)


def get_flights(path='dataset/flights.csv'):
    """Return a generator that yields direct Flight objects."""

    with open(path, 'rt', encoding="utf8") as fd:
        reader = csv.reader(fd)
        for row in reader:
            origin = row[2]  # IATA code of source ...
            destination = row[4]  # ... and destination airport.
            nstops = int(row[7])  # Number of stops; zero for direct.
            if not nstops:
                yield Flight(origin=origin, destination=destination)


def timeit(func):
    """Decorator to time a function."""

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter() - start
        print(f"Time elapsed: {end:.6f} seconds")
        return result

    return wrapper
