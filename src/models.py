import collections

Airport = collections.namedtuple('Airport', 'code name country latitude longitude')
Flight = collections.namedtuple('Flight', 'origin destination')
Route = collections.namedtuple('Route', 'price path')
