import unittest
from hinanbasho.scraper import Scraper
from requests import ConnectionError
from requests import HTTPError
from requests import RequestException
from requests import Timeout
from unittest.mock import Mock, patch


class TestScraper(unittest.TestCase):
    @patch("hinanbasho.scraper.requests")
    def test_lists(self, mock_requests):
        csv_content = (
            "施設名,郵便番号,住所,電話番号,ファクス番号,地図の緯度,地図の経度"
            + "\r\n"
            + "常磐公園,070-0044,北海道旭川市常磐公園,0166-23-8961,なし,43.7748548,142.3578223"
            + "\r\n"
            + "豊西会館,074-1182,北海道旭川市神居町豊里,なし,なし,,"
            + "\r\n"
        )
        mock_requests.get.return_value = Mock(
            status_code=200, content=csv_content.encode("cp932")
        )
        expect = [
            {
                "site_name": "常磐公園",
                "postal_code": "070-0044",
                "address": "北海道旭川市常磐公園",
                "phone_number": "0166-23-8961",
                "latitude": 43.7748548,
                "longitude": 142.3578223,
            }, {
                "site_name": "豊西会館",
                "postal_code": "074-1182",
                "address": "北海道旭川市神居町豊里",
                "phone_number": "なし",
                "latitude": 43.6832208,
                "longitude": 142.1762534,
            },
        ]
        downloaded_csv = Scraper("http://dummy.local")
        self.assertEqual(downloaded_csv.lists, expect)

        mock_requests.get.side_effect = Timeout("Dummy Error.")
        with self.assertRaises(RequestException):
            Scraper("http://dummy.local")

        mock_requests.get.side_effect = HTTPError("Dummy Error.")
        with self.assertRaises(RequestException):
            Scraper("http://dummy.local")

        mock_requests.get.side_effect = ConnectionError("Dummy Error.")
        with self.assertRaises(RequestException):
            Scraper("http://dummy.local")


if __name__ == "__main__":
    unittest.main()
