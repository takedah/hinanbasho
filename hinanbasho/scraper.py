import io
import numpy as np
import pandas as pd
import requests


class DownloadedCSV:
    """旭川市オープンデータライブラリからCSVをダウンロードしてテキスト要素の二次元配列に格納する

    Attributes:
        lists(list of lists): CSVを二次元配列に変換したデータ

    """

    def __init__(self, url: str):
        """
        Args:
            url (str): CSVのURL

        """
        self.__lists = list()

        response = requests.get(url)
        csv_content = io.BytesIO(response.content)

        df = pd.read_csv(csv_content, encoding="cp932", header=None, dtype=str)
        df.replace(np.nan, "", inplace=True)

        self.__lists = df.values.tolist()

    @property
    def lists(self) -> list:
        return self.__lists


if __name__ == "__main__":
    url = (
        "https://www.city.asahikawa.hokkaido.jp/kurashi/320/321/d053843_d/fil/"
        + "012041_hinanbasho_list.csv"
    )
    downloaded_csv = DownloadedCSV(url)
    for row in downloaded_csv.lists:
        print(row)
