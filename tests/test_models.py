import unittest

from hinanbasho.errors import LocationError
from hinanbasho.models import (
    AreaAddress,
    AreaAddressFactory,
    CurrentLocation,
    EvacuationSite,
    EvacuationSiteFactory
)

test_evacuation_site_data = [
    {
        "site_id": 1,
        "site_name": "常磐公園",
        "postal_code": "070-0044",
        "address": "北海道旭川市常磐公園",
        "phone_number": "0166-23-8961",
        "latitude": 43.7748548,
        "longitude": 142.3578223,
    },
    {
        "site_id": 2,
        "site_name": "花咲スポーツ公園",
        "postal_code": "071-0901",
        "address": "北海道旭川市花咲町1〜5丁目",
        "phone_number": "0166-52-1934",
        "latitude": 43.78850998,
        "longitude": 142.3681739,
    },
]
test_area_address_data = [
    {
        "postal_code": "0700044",
        "area_name": "北海道旭川市常磐公園",
    },
]


class TestEvacuationSite(unittest.TestCase):
    def setUp(self):
        self.evacuation_site = EvacuationSite(**test_evacuation_site_data[0])

    def test_site_id(self):
        self.assertEqual(self.evacuation_site.site_id, 1)

    def test_site_name(self):
        self.assertEqual(self.evacuation_site.site_name, "常磐公園")

    def test_postal_code(self):
        self.assertEqual(self.evacuation_site.postal_code, "070-0044")

    def test_address(self):
        self.assertEqual(self.evacuation_site.address, "北海道旭川市常磐公園")

    def test_phone_number(self):
        self.assertEqual(self.evacuation_site.phone_number, "0166-23-8961")

    def test_latitude(self):
        self.assertEqual(self.evacuation_site.latitude, 43.7748548)

    def test_longitude(self):
        self.assertEqual(self.evacuation_site.longitude, 142.3578223)


class TestEvacuationSiteFactory(unittest.TestCase):
    def test_create(self):
        factory = EvacuationSiteFactory()
        # EvacuationSiteクラスのオブジェクトが生成できるか確認する。
        evacuation_site = factory.create(test_evacuation_site_data[0])
        self.assertTrue(isinstance(evacuation_site, EvacuationSite))


class TestCurrentLocation(unittest.TestCase):
    def setUp(self):
        factory = EvacuationSiteFactory()
        factory.create(test_evacuation_site_data[0])
        self.evacuation_site = factory.items[0]
        current_latitude = test_evacuation_site_data[1]["latitude"]
        current_longitude = test_evacuation_site_data[1]["longitude"]
        self.current_location = CurrentLocation(
            latitude=current_latitude, longitude=current_longitude
        )

    def test_get_distance_to(self):
        result = self.current_location.get_distance_to(self.evacuation_site)
        self.assertEqual(result, 1732.87)

    def test_init(self):
        with self.assertRaises(LocationError):
            CurrentLocation(latitude="hoge", longitude="fuga")


class TestAreaAddress(unittest.TestCase):
    def setUp(self):
        self.area_address = AreaAddress(**test_area_address_data[0])

    def test_postal_code(self):
        self.assertEqual(self.area_address.postal_code, "070-0044")

    def test_area_address(self):
        self.assertEqual(self.area_address.area_name, "北海道旭川市常磐公園")


class TestAreaAddressFactory(unittest.TestCase):
    def test_create(self):
        factory = AreaAddressFactory()
        # AreaAddressクラスのオブジェクトが生成できるか確認する。
        area_address = factory.create(test_area_address_data[0])
        self.assertTrue(isinstance(area_address, AreaAddress))


if __name__ == "__main__":
    unittest.main()
