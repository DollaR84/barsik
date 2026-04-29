from contextlib import asynccontextmanager
import logging
from typing import Literal, overload

from geopy import Location
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from geopy.distance import lonlat
from geopy.distance import distance as geopy_distance

from shapely.geometry import Point, Polygon, mapping
from shapely.ops import transform

from pyproj import Transformer

from barsik.config.adapters import GeoConfig


class GeoOSM:

    def __init__(self, app_name: str, config: GeoConfig):
        self.app_name = app_name
        self.config: GeoConfig = config

    @asynccontextmanager
    async def get_locator(self) -> Nominatim:
        yield Nominatim(
            user_agent=self.app_name,
            timeout=self.config.location_timeout,
            adapter_factory=AioHTTPAdapter,
        )

    async def _get_location(self, coordinates: str, lang: str | bool = False) -> Location:
        async with self.get_locator() as locator:
            location = await locator.reverse(coordinates, language=lang)
            return location

    async def get_location(self, coordinates: str, lang: str | bool = False) -> str:
        location = await self._get_location(coordinates, lang)
        result: str = location.raw["display_name"]
        return result

    @overload
    async def get_address(
            self,
            coordinates: str,
            lang: str = "en",
            return_data: Literal["full"] = "full",
    ) -> dict[str, str]:
        ...

    @overload
    async def get_address(
            self,
            coordinates: str,
            lang: str = "en",
            return_data: Literal[
                "country", "country_code", "city",
                "municipality", "district", "state", "postcode",
                "road", "residential", "suburb", "borough",
            ] = "city",
    ) -> str:
        ...

    async def get_address(
            self, coordinates: str,
            lang: str = "en",
            return_data: Literal[
                "full", "country", "country_code", "city",
                "municipality", "district", "state", "postcode",
                "road", "residential", "suburb", "borough",
            ] = "full",
    ) -> dict[str, str] | str:
        location = await self._get_location(coordinates, lang)
        address: dict[str, str] = location.raw["address"]
        if return_data == "full":
            return address

        data: str | None = address.get(return_data)
        if data is None:
            data = ""
        return data

    @overload
    async def search(self, search_text: str, lang: str | bool, exactly_one: Literal[False]) -> list[str] | None:
        ...

    @overload
    async def search(self, search_text: str, lang: str | bool, exactly_one: Literal[True]) -> str | None:
        ...

    async def search(
            self, search_text: str,
            lang: str | bool = False,
            exactly_one: bool = False,
    ) -> str | list[str] | None:
        # pylint: disable=simplifiable-if-expression
        results = await self._search(search_text, lang, exactly_one=True if exactly_one else False)

        if not results:
            return None
        if isinstance(results, Location):
            result: str = results.address
            return result
        return [result.address for result in results]

    @overload
    async def _search(self, search_text: str, lang: str | bool, exactly_one: Literal[False]) -> list[Location] | None:
        ...

    @overload
    async def _search(self, search_text: str, lang: str | bool, exactly_one: Literal[True]) -> Location | None:
        ...

    async def _search(
            self, search_text: str,
            lang: str | bool = False,
            exactly_one: bool = False,
    ) -> Location | list[Location] | None:
        async with self.get_locator() as locator:
            try:
                results = await locator.geocode(search_text, exactly_one=exactly_one, language=lang)
            except GeocoderTimedOut as e:
                logger = logging.getLogger()
                logger.error("geocode fail with error: %s", e)
                results = None

            return results

    async def get_coordinates(
            self,
            address: str,
            lang: str | bool = False
    ) -> list[float] | None:
        result = None
        location = await self._search(address, lang, exactly_one=True)
        if location:
            if isinstance(location, list):
                location = location[0]
            result = [location.latitude, location.longitude]
        return result

    def distance(
            self,
            point1: list[str | float],
            point2: list[str | float],
            units: Literal["km", "m", "mi"] = "km",
            ndigits: int = 3,
    ) -> float:
        p1: tuple[float, ...] = self.convert_point(point1)
        p_1 = lonlat(*p1)

        p2: tuple[float, ...] = self.convert_point(point2)
        p_2 = lonlat(*p2)

        dist_obj = geopy_distance(p_1, p_2)
        dist = getattr(dist_obj, units)
        if dist is None:
            dist = dist_obj.km

        if dist and dist < 1:
            dist = dist_obj.m
            ndigits = 2

        dist = round(dist, ndigits=ndigits)
        return float(dist)

    def from_polygon(self, polygon: Polygon) -> list[str]:
        data = mapping(polygon)
        return list(data["coordinates"][0])

    def to_polygon(self, points: list[list[str | float]]) -> Polygon:
        clean_points = [self.convert_point(p, "tuple") for p in points]
        return Polygon(clean_points)

    def check_inside_polygon(
            self,
            polygon: list[list[str | float]],
            point: list[str | float],
            is_swap_coordinates: bool = True,
    ) -> bool:
        polygon_ = self.to_polygon(polygon)
        p = self.convert_point(point, "list")

        if is_swap_coordinates:
            point_obj = Point(*p)
        else:
            point_obj = Point(*[p[1], p[0]])

        return bool(polygon_.contains(point_obj))

    @overload
    def convert_point(self, point: list[str | float], return_type: Literal["tuple"] = "tuple") -> tuple[float, ...]:
        ...

    @overload
    def convert_point(self, point: list[str | float], return_type: Literal["list"]) -> list[float]:
        ...

    @overload
    def convert_point(self, point: list[str | float], return_type: Literal["point"]) -> Point:
        ...

    def convert_point(
            self,
            point: list[str | float],
            return_type: Literal["tuple", "list", "point"] = "tuple",
    ) -> tuple[float, ...] | list[float] | Point:
        p = list(map(float, point))

        if return_type == "tuple":
            return tuple(p)
        if return_type == "list":
            return p
        if return_type == "point":
            return Point(*p)
        raise ValueError("incorrect set return type")

    def check_inside_distance1(self, center_point: list[str | float], distance: int, point: list[str | float]) -> bool:
        center = self.convert_point(center_point, "point")
        p = self.convert_point(point, "point")

        buffer = self.buffer_in_meters(center, distance)
        return buffer.contains(p)  # p.within(buffer)

    def buffer_in_meters(self, center_point: Point, radius: int) -> Polygon:
        transformer_to = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        transformer_back = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

        pt_meters = transform(transformer_to.transform, center_point)
        buffer_meters = pt_meters.buffer(radius)

        return transform(transformer_back.transform, buffer_meters)

    def check_inside_distance2(self, center_point: list[str | float], distance: int, point: list[str | float]) -> bool:
        center = self.convert_point(center_point, "point")
        p = self.convert_point(point, "point")

        return center.distance(p) < distance
