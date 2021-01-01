import io
import numpy as np
import pandas as pd
import requests


class Scraper:
    """旭川市オープンデータライブラリからCSVをダウンロードしてテキスト要素の二次元配列に格納する

    Attributes:
        lists(list of dicts): CSVの各行を辞書にしてリストに格納したデータ

    """

    def __init__(self, url: str):
        """
        Args:
            url (str): CSVのURL

        """
        self.__lists = list()
        response = requests.get(url)
        csv_content = io.BytesIO(response.content)
        df = pd.read_csv(csv_content, encoding="cp932", header=0, dtype=str)
        df.replace(np.nan, "", inplace=True)
        for row in df.values.tolist():
            # オープンデータの豊西会館だけ緯度経度が抜けているので対策する
            if row[0] == "豊西会館":
                latitude = 43.6832208
                longitude = 142.1762534
            else:
                latitude = float(row[5])
                longitude = float(row[6])
            self.__lists.append(
                {
                    "site_name": row[0],
                    "postal_code": row[1],
                    "address": row[2],
                    "phone_number": row[3],
                    "latitude": latitude,
                    "longitude": longitude,
                }
            )

    @property
    def lists(self) -> list:
        return self.__lists
