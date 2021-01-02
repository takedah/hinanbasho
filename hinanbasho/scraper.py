import io
import numpy as np
import pandas as pd
import requests
from hinanbasho.config import Config


class Scraper:
    """旭川市オープンデータライブラリからCSVをダウンロードしてテキスト要素の二次元配列に格納する

    Attributes:
        lists(list of dicts): CSVの各行を辞書にしてリストに格納したデータ

    """

    def __init__(self):
        self.__lists = list()
        # 旭川市ホームページのTLS証明書のDH鍵長に問題があるためセキュリティを下げて回避する
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH"
        response = requests.get(Config.OPENDATA_URL)
        csv_content = io.BytesIO(response.content)
        df = pd.read_csv(csv_content, encoding="cp932", header=0, dtype=str)
        df.replace(np.nan, "", inplace=True)
        i = 0
        for row in df.values.tolist():
            # CSVの行数をデータベースのキーにできるようにする
            csv_row_number = i + 1
            # オープンデータの豊西会館だけ緯度経度が抜けているので対策する
            if row[0] == "豊西会館":
                latitude = 43.6832208
                longitude = 142.1762534
            else:
                latitude = float(row[5])
                longitude = float(row[6])
            self.__lists.append(
                {
                    "site_id": csv_row_number,
                    "site_name": row[0],
                    "postal_code": row[1],
                    "address": row[2],
                    "phone_number": row[3],
                    "latitude": latitude,
                    "longitude": longitude,
                }
            )
            i += 1

    @property
    def lists(self) -> list:
        return self.__lists
