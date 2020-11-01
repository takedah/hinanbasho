import unittest
from hinanbasho.models import EvacuationSite
from hinanbasho.models import EvacuationSiteFactory
from hinanbasho.models import EvacuationSiteService
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
]


class TestEvacuationSite(unittest.TestCase):
    def setUp(self):
        self.evacuation_site = EvacuationSite(**test_data[0])

    def test_name(self):
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
        evacuation_site = factory.create(test_data[0])
        self.assertTrue(isinstance(evacuation_site, EvacuationSite))


class TestEvacuationSiteService(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.factory = EvacuationSiteFactory()
        for d in test_data:
            self.factory.create(d)
        self.db = DB(DB.TEST_DATABASE_URL)
        self.service = EvacuationSiteService(self.db)

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
