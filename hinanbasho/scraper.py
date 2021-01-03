import io
import numpy as np
import pandas as pd
import requests
from hinanbasho.config import Config


class OpenData:
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


class PostOfficeCSV:
    """
    日本郵便株式会社WebサイトからローカルにダウンロードしたCSVファイルから
    データを抽出する

    Attributes:
        lists(list of dicts): CSVの各行を辞書にしてリストに格納したデータ

    """

    def __init__(self):
        self.__lists = list()
        df = pd.read_csv(
            Config.POST_OFFICE_CSV_PATH, encoding="cp932", header=None, dtype=str
        )
        df.replace(np.nan, "", inplace=True)

        i = 0
        data_length = len(df.values.tolist())
        tmp = {
            "postal_code": None,
            "area_address": None,
        }
        duplicate_key = ""
        for row in df.values.tolist():
            postal_code = row[2]
            area_address = row[8]
            if i == 0:
                # CSV先頭行
                # 一つ前の行までのデータを一時的に保存するもの。
                tmp = {
                    "postal_code": postal_code,
                    "area_address": area_address,
                }
                # 一つ前の行までのデータの郵便番号。
                duplicate_key = postal_code
            elif i < data_length - 1:
                # CSV2行目以降最終行の1行前まで
                # 町域が複数行に分かれている場合の処理
                # 前の行と現在の行の郵便番号が同一かどうかで判断する。
                if postal_code == duplicate_key:
                    # 町域が複数行に分かれている場合は町域を追記。
                    tmp["area_address"] = tmp["area_address"] + area_address
                else:
                    # 町域が複数行に分かれていない場合に初めてデータを抽出。
                    self.__lists.append(tmp)
                    # 一時保存データを現在の行のデータで初期化する。
                    tmp = {
                        "postal_code": postal_code,
                        "area_address": area_address,
                    }
                    duplicate_key = postal_code
            else:
                # CSV最終行
                self.__lists.append(tmp)
                self.__lists.append(
                    {
                        "postal_code": postal_code,
                        "area_address": area_address,
                    }
                )

            i += 1

    @property
    def lists(self) -> list:
        return self.__lists
