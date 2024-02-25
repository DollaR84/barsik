from contextlib import asynccontextmanager
from functools import partial
import logging
from typing import Literal

from barsik.config import BaseConfig

from geopy import Location
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from geopy.distance import lonlat
from geopy.distance import distance as geopy_distance

from shapely.geometry import Point, Polygon, mapping
from shapely.ops import transform

import pyproj


class GeoOSM:

    def __init__(self, config: BaseConfig):
        self.cfg: BaseConfig = config

    @asynccontextmanager
    async def get_locator(self) -> Nominatim:
        yield Nominatim(
            user_agent=self.cfg.geo.app_name,
            timeout=self.cfg.geo.location_timeout,
            adapter_factory=AioHTTPAdapter,
        )

    async def _get_location(self, coordinates: str, lang: str | bool = False) -> Location:
        async with self.get_locator() as locator:
            location = await locator.reverse(coordinates, language=lang)
            return location

    async def get_location(self, coordinates: str, lang: str | bool = False) -> str:
        location = await self._get_location(coordinates, lang)
        return location.raw["display_name"]

    async def get_address(
            self, coordinates: str,
            lang: str = "en",
            return_data: Literal[
                "full", "country", "country_code", "city",
                "municipality", "district", "state", "postcode",
                "road", "residential", "suburb", "borough",
            ] = "full",
    ) -> dict | str:
        location = await self._get_location(coordinates, lang)
        address = location.raw["address"]
        if return_data == "full":
            return address
        return address.get(return_data)

    async def search(
            self, search_text: str,
            lang: str | bool = False,
            exactly_one: bool = False
    ) -> str | list[str]:
        return await self._search(search_text, lang, exactly_one=exactly_one, return_type="address")

    async def _search(
            self, search_text: str,
            lang: str | bool = False,
            exactly_one: bool = False,
            return_type: Literal["raw", "address"] = "raw"
    ) -> str | list[str] | Location:
        async with self.get_locator() as locator:
            try:
                results = await locator.geocode(search_text, exactly_one=exactly_one, language=lang)
            except GeocoderTimedOut as e:
                logger = logging.getLogger()
                logger.error("geocode fail with error: %s", e)
                results = None
            finally:
                if results and return_type == "address":
                    results = results.address if exactly_one else [result.address for result in results]

            return results

    async def get_coordinates(
            self,
            address: str,
            lang: str | bool = False
    ) -> tuple[str, str] | None:
        result = await self._search(address, lang, exactly_one=True)
        if result:
            result = [result.latitude, result.longitude]
        return result

    def distance(
            self,
            point1: list, point2: list,
            units: Literal["km", "m", "mi"] = "km",
            ndigits: int = 3,
    ) -> float | str:
        if isinstance(point1[0], float) and isinstance(point1[1], float):
            point1 = lonlat(*point1)
        else:
            point1 = ", ".join(point1)

        if isinstance(point2[0], float) and isinstance(point2[1], float):
            point2 = lonlat(*point2)
        else:
            point2 = ", ".join(point2)

        dist = geopy_distance(point1, point2)
        try:
            dist = getattr(dist, units)
        except Exception:
            dist = dist.km

        if dist < 1:
            dist = dist.m
            ndigits = 2

        dist = round(dist, ndigits=ndigits)
        return float(dist)

    def from_polygon(self, polygon: Polygon) -> list:
        data = mapping(polygon)
        return list(data["coordinates"][0])

    def to_polygon(self, points: list) -> Polygon:
        return Polygon(points)

    def check_inside_polygon(self, polygon: list, point: list, is_swap_coordinates: bool = True) -> bool:
        polygon = self.to_polygon(polygon)

        if isinstance(point[0], str) and isinstance(point[1], str):
            point = list(map(float, point))

        if is_swap_coordinates:
            point = Point(*point)
        else:
            point = Point(*[point[1], point[0]])

        return polygon.contains(point)

    def convert_point(self, point: list, return_type: Literal["list", "point"]):
        if isinstance(point[0], str) and isinstance(point[1], str):
            point = list(map(float, point))

        if return_type == "list":
            return point
        elif return_type == "point":
            return Point(point)

    def check_inside_distance1(self, center_point: list, distance: int, point: list) -> bool:
        center_point = self.convert_point(center_point, "list")
        point = self.convert_point(point, "list")

        buffer = self.buffer_in_meters(center_point, distance)
        return buffer.contains(point)  # point.within(buffer)

    def buffer_in_meters(self, center_point: Point, radius: int):
        proj_meters = pyproj.Proj(init="epsg:3857")
        proj_latlng = pyproj.Proj(init="epsg:4326")

        project_to_meters = partial(pyproj.transform, proj_latlng, proj_meters)
        project_to_latlng = partial(pyproj.transform, proj_meters, proj_latlng)

        pt_meters = transform(project_to_meters, center_point)
        buffer_meters = pt_meters.buffer(radius)
        buffer_latlng = transform(project_to_latlng, buffer_meters)

        return buffer_latlng

    def check_inside_distance2(self, center_point: list, distance: int, point: list) -> bool:
        center_point = self.convert_point(center_point, "point")
        point = self.convert_point(point, "point")

        return center_point.distance(point) < distance
