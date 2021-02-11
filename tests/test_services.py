import unittest

from hinanbasho.db import DB
from hinanbasho.models import (
    AreaAddressFactory,
    CurrentLocation,
    EvacuationSite,
    EvacuationSiteFactory
)
from hinanbasho.services import AreaAddressService, EvacuationSiteService

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
        "postal_code": "070-0901",
        "address": "北海道旭川市花咲町1〜5丁目",
        "phone_number": "0166-52-1934",
        "latitude": 43.78850998,
        "longitude": 142.3681739,
    },
    {
        "site_id": 3,
        "site_name": "イオンモール旭川西店(3階駐車場及び屋上駐車場)",
        "postal_code": "070-0823",
        "address": "北海道旭川市緑町23丁目",
        "phone_number": "0166-59-7900",
        "latitude": 43.79368448,
        "longitude": 142.325844,
    },
    {
        "site_id": 4,
        "site_name": "東光スポーツ公園",
        "postal_code": "078-8361",
        "address": "北海道旭川市東光21～27条7・8丁目・東光22～27条9丁目",
        "phone_number": "0166-52-1934",
        "latitude": 43.73178028,
        "longitude": 142.4120177,
    },
    {
        "site_id": 5,
        "site_name": "クリスタルパーク",
        "postal_code": "070-8003",
        "address": "北海道旭川市神楽3条7・8丁目",
        "phone_number": "0166-74-8005",
        "latitude": 43.75891797,
        "longitude": 142.3520454,
    },
    {
        "site_id": 6,
        "site_name": "忠和公園",
        "postal_code": "070-8021",
        "address": "北海道旭川市神居町忠和",
        "phone_number": "0166-69-2345",
        "latitude": 43.78344692,
        "longitude": 142.3164453,
    },
]
test_area_address_data = [
    {
        "postal_code": "0700044",
        "area_name": "常磐公園",
    },
    {
        "postal_code": "0700901",
        "area_name": "花咲町",
    },
    {
        "postal_code": "0700823",
        "area_name": "緑町",
    },
    {
        "postal_code": "0788361",
        "area_name": "東光２１条",
    },
    {
        "postal_code": "0708003",
        "area_name": "神楽３条",
    },
    {
        "postal_code": "0708021",
        "area_name": "神居町忠和",
    },
]


class TestEvacuationSiteService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.factory = EvacuationSiteFactory()
        for row in test_evacuation_site_data:
            self.factory.create(**row)
        self.db = DB()
        self.service = EvacuationSiteService(self.db)
        self.current_location = CurrentLocation(
            latitude=43.7708179, longitude=142.3628371
        )

    @classmethod
    def tearDownClass(self):
        self.db.close()

    def test_create(self):
        self.service.truncate()
        for item in self.factory.items:
            self.assertTrue(self.service.create(item))
        self.db.commit()

    def test_get_all(self):
        for item in self.service.get_all():
            self.assertTrue(isinstance(item, EvacuationSite))

    def test_get_near_sites(self):
        near_sites = self.service.get_near_sites(self.current_location)
        # 一番近い避難場所
        self.assertEqual(near_sites[0]["order"], 1)
        self.assertEqual(near_sites[0]["site"].site_name, "常磐公園")
        self.assertEqual(near_sites[0]["distance"], 0.6)
        # 二番目に近い避難場所
        self.assertEqual(near_sites[1]["order"], 2)
        self.assertEqual(near_sites[1]["site"].site_name, "クリスタルパーク")
        self.assertEqual(near_sites[1]["distance"], 1.6)
        # 一番遠い避難場所
        self.assertEqual(near_sites[-1]["order"], 5)
        self.assertEqual(near_sites[-1]["site"].site_name, "忠和公園")
        self.assertEqual(near_sites[-1]["distance"], 4)

    def test_find_by_site_id(self):
        site = self.service.find_by_site_id(3)
        self.assertEqual(site[0].site_name, "イオンモール旭川西店(3階駐車場及び屋上駐車場)")

    def test_get_area_names(self):
        expect = ["花咲町", "常磐公園", "神楽３条", "神居町忠和", "東光２１条", "緑町"]
        self.assertEqual(self.service.get_area_names(), expect)

    def test_find_by_area_name(self):
        area_sites = self.service.find_by_area_name("花咲町")
        self.assertEqual(area_sites[0].site_name, "花咲スポーツ公園")

    def test_find_by_site_name(self):
        results = self.service.find_by_site_name("花咲")
        self.assertEqual(results[0].site_name, "花咲スポーツ公園")


class TestAreaAddressService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.factory = AreaAddressFactory()
        for row in test_area_address_data:
            self.factory.create(**row)
        self.db = DB()
        self.service = AreaAddressService(self.db)

    @classmethod
    def tearDownClass(self):
        self.db.close()

    def test_create(self):
        self.service.truncate()
        for item in self.factory.items:
            self.assertTrue(self.service.create(item))
        self.db.commit()


if __name__ == "__main__":
    unittest.main()
