# utils.py
from geopy.distance import distance as geopy_distance

def calculate_distance(lat1, lon1, lat2, lon2):
    return geopy_distance((lat1, lon1), (lat2, lon2)).km
