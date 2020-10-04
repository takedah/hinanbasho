import unittest
from hinanbasho.scraper import DownloadedCSV
from requests import ConnectionError
from requests import HTTPError
from requests import RequestException
from requests import Timeout
from unittest.mock import Mock, patch


class TextDownloadedCSV(unittest.TestCase):
    @patch("hinanbasho.scraper.requests")
    def test_lists(self, mock_requests):
        csv_content = "a,b,c" + "\r\n" + "1,2,3" + "\r\n"
        mock_requests.get.return_value = Mock(
            status_code=200, content=csv_content.encode()
        )
        expect = [["a", "b", "c"], ["1", "2", "3"]]
        downloaded_csv = DownloadedCSV("http://dummy.local")
        self.assertEqual(downloaded_csv.lists, expect)

        mock_requests.get.side_effect = Timeout("Dummy Error.")
        with self.assertRaises(RequestException):
            DownloadedCSV("http://dummy.local")

        mock_requests.get.side_effect = HTTPError("Dummy Error.")
        with self.assertRaises(RequestException):
            DownloadedCSV("http://dummy.local")

        mock_requests.get.side_effect = ConnectionError("Dummy Error.")
        with self.assertRaises(RequestException):
            DownloadedCSV("http://dummy.local")


if __name__ == "__main__":
    unittest.main()
