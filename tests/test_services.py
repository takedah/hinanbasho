import unittest
from hinanbasho.models import CurrentLocation
from hinanbasho.models import EvacuationSite
from hinanbasho.models import EvacuationSiteFactory
from hinanbasho.services import EvacuationSiteService
from hinanbasho.db import DB


test_data = [
    {
        "site_name": "常磐公園",
        "postal_code": "070-0044",
        "address": "北海道旭川市常磐公園",
        "phone_number": "0166-23-8961",
        "latitude": 43.7748548,
        "longitude": 142.3578223,
    },
    {
        "site_name": "花咲スポーツ公園",
        "postal_code": "071-0901",
        "address": "北海道旭川市花咲町1〜5丁目",
        "phone_number": "0166-52-1934",
        "latitude": 43.78850998,
        "longitude": 142.3681739,
    },
    {
        "site_name": "イオンモール旭川西店(3階駐車場及び屋上駐車場)",
        "postal_code": "070-0823",
        "address": "北海道旭川市緑町23丁目",
        "phone_number": "0166-59-7900",
        "latitude": 43.79368448,
        "longitude": 142.325844,
    },
    {
        "site_name": "東光スポーツ公園",
        "postal_code": "078-8361",
        "address": "北海道旭川市東光21～27条7・8丁目・東光22～27条9丁目",
        "phone_number": "0166-52-1934",
        "latitude": 43.73178028,
        "longitude": 142.4120177,
    },
    {
        "site_name": "クリスタルパーク",
        "postal_code": "070-8003",
        "address": "北海道旭川市神楽3条7・8丁目",
        "phone_number": "0166-74-8005",
        "latitude": 43.75891797,
        "longitude": 142.3520454,
    },
    {
        "site_name": "忠和公園",
        "postal_code": "070-8021",
        "address": "北海道旭川市神居町忠和",
        "phone_number": "0166-69-2345",
        "latitude": 43.78344692,
        "longitude": 142.3164453,
    },
]


class TestEvacuationSiteService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.factory = EvacuationSiteFactory()
        for d in test_data:
            self.factory.create(d)
        self.db = DB(DB.TEST_DATABASE_URL)
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
        self.assertEqual(near_sites[0][0].site_name, "常磐公園")
        self.assertEqual(near_sites[0][1], 603.69)
        self.assertEqual(near_sites[1][0].site_name, "クリスタルパーク")
        self.assertEqual(near_sites[1][1], 1583.51)


if __name__ == "__main__":
    unittest.main()
