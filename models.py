from pydantic import BaseModel


class Airport(BaseModel):
    code: str
    name: str
    country: str
    latitude: float
    longitude: float

    class Config:
        frozen = True


class Flight(BaseModel):
    origin: str
    destination: str

    class Config:
        frozen = True


class Route(BaseModel):
    price: float
    path: list[Airport]

    class Config:
        frozen = True

    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.price == other.price

    def __gt__(self, other):
        return self.price > other.price

    def __le__(self, other):
        return self.price <= other.price

    def __ge__(self, other):
        return self.price >= other.price


