import unittest
from unittest.mock import Mock, patch

from requests import ConnectionError, HTTPError, RequestException, Timeout

from hinanbasho.scraper import OpenData, PostOfficeCSV


class TestOpenData(unittest.TestCase):
    @patch("hinanbasho.scraper.requests")
    def test_lists(self, mock_requests):
        csv_content = (
            "施設名,郵便番号,住所,電話番号,ファクス番号,地図の緯度,地図の経度"
            + "\r\n"
            + "常磐公園,070-0044,北海道旭川市常磐公園,0166-23-8961,なし,43.7748548,"
            + "142.3578223"
            + "\r\n"
            + "豊西会館,074-1182,北海道旭川市神居町豊里,なし,なし,,"
            + "\r\n"
            + "花咲スポーツ公園,071-0901,北海道旭川市花咲町1～5丁目,0166-52-1934,なし,"
            + "43.78850998,142.3681739"
            + "\r\n"
        )
        mock_requests.get.return_value = Mock(
            status_code=200, content=csv_content.encode("cp932")
        )
        expect = [
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
                "site_name": "豊西会館",
                "postal_code": "074-1182",
                "address": "北海道旭川市神居町豊里",
                "phone_number": "なし",
                "latitude": 43.6832208,
                "longitude": 142.1762534,
            },
            {
                "site_id": 3,
                "site_name": "花咲スポーツ公園",
                "postal_code": "070-0901",
                "address": "北海道旭川市花咲町1～5丁目",
                "phone_number": "0166-52-1934",
                "latitude": 43.78850998,
                "longitude": 142.3681739,
            },
        ]
        open_data = OpenData()
        self.assertEqual(open_data.lists, expect)

        mock_requests.get.side_effect = Timeout("Dummy Error.")
        with self.assertRaises(RequestException):
            OpenData()

        mock_requests.get.side_effect = HTTPError("Dummy Error.")
        with self.assertRaises(RequestException):
            OpenData()

        mock_requests.get.side_effect = ConnectionError("Dummy Error.")
        with self.assertRaises(RequestException):
            OpenData()


class TestPostOfficeCSV(unittest.TestCase):
    def test_lists(self):
        post_office_csv = PostOfficeCSV()
        # 先頭行
        expect = {
            "postal_code": "0600000",
            "area_name": "以下に掲載がない場合",
        }
        self.assertEqual(post_office_csv.lists[0], expect)
        # 1382行目
        expect = {
            "postal_code": "0700055",
            "area_name": "５条西",
        }
        self.assertEqual(post_office_csv.lists[1382], expect)
        # 最終行
        expect = {
            "postal_code": "0861834",
            "area_name": "礼文町",
        }
        self.assertEqual(post_office_csv.lists[-1], expect)


if __name__ == "__main__":
    unittest.main()
