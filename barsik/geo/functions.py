from math import radians, sin, cos, sqrt, atan2

from aiogram import types


def location_to_str(message: types.Message) -> str:
    coordinates = message.location
    return ", ".join([str(coordinates["latitude"]), str(coordinates["longitude"])])


def polygon_from_string(polygon: str, is_swap_coordinates: bool) -> list:
    polygon = polygon.strip()
    if polygon.startswith("POLYGON"):
        polygon = polygon.replace("POLYGON", "")
    polygon = polygon.replace("(", "").replace(")", "")

    points = polygon.split(",")
    points = [list(map(float, point.split(" "))) for point in points]

    if is_swap_coordinates:
        for point in points:
            point[0], point[1] = point[1], point[0]

    return points


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Radius of the Earth in meters
    r = 6371000.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    res_distance = r * c

    return res_distance


def is_point_inside_radius(
        center_lat: float, center_lon: float,
        point_lat: float, point_lon: float,
        radius: int,
) -> bool:
    res_distance = haversine(center_lat, center_lon, point_lat, point_lon)
    return res_distance <= radius
