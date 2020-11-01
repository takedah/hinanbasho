from datetime import datetime
from datetime import timedelta
from datetime import timezone
from hinanbasho.factory import Factory
from hinanbasho.db import DatabaseError
from hinanbasho.db import DataError
from hinanbasho.logs import DBLog


class EvacuationSite:
    """避難場所のデータモデル

    Attributes:
        site_name (str): 避難場所名
        postal_code (str): 避難場所の郵便番号
        address (str): 避難場所の住所
        phone_number (str): 避難場所の電話番号
        latitude (float): 避難場所の緯度
        longitude (float): 避難場所の経度

    """

    def __init__(self, **kwargs: dict):
        """
        Args:
            **kwargs: 避難場所の情報を格納したディクショナリ

        """
        self.__site_name = str(kwargs["site_name"])
        self.__postal_code = str(kwargs["postal_code"])
        self.__address = str(kwargs["address"])
        self.__phone_number = str(kwargs["phone_number"])
        self.__latitude = float(kwargs["latitude"])
        self.__longitude = float(kwargs["longitude"])

    @property
    def site_name(self) -> str:
        return self.__site_name

    @property
    def postal_code(self) -> str:
        return self.__postal_code

    @property
    def address(self) -> str:
        return self.__address

    @property
    def phone_number(self) -> str:
        return self.__phone_number

    @property
    def latitude(self) -> float:
        return self.__latitude

    @property
    def longitude(self) -> float:
        return self.__longitude


class EvacuationSiteFactory(Factory):
    """避難場所モデルを作成する。

    Attributes:
        items (list of :obj:`EvacuationSite`): 避難場所オブジェクトのリスト

    """

    def __init__(self):
        self.__items = list()

    @property
    def items(self) -> list:
        return self.__items

    def _create_item(self, row: dict):
        """避難場所オブジェクトを作成する。

        Args:
            row (dict): 避難場所情報を表すディクショナリ

        """
        return EvacuationSite(**row)

    def _register_item(self, item: EvacuationSite):
        """避難場所オブジェクトをリストに追加。

        Args:
            item (:obj:`EvacuationSite`): 避難場所オブジェクト

        """
        self.__items.append(item)


class EvacuationSiteService:
    """避難場所サービス"""

    def __init__(self, db):
        """
        Args:
            db(:obj:`DB`): データベース操作をラップしたオブジェクト

        """
        self.__db = db
        self.__table_name = "evacuation_sites"
        self.__logger = DBLog()

    def truncate(self):
        """スケジュールテーブルのデータを全削除"""
        state = "TRUNCATE TABLE " + self.__table_name + " RESTART IDENTITY;"
        self.__db.execute(state)

    def create(self, evacuation_site: EvacuationSite):
        """データベースへ避難場所データを保存

        Args:
            evacuation_site (obj:`EvacuationSite`): 避難場所データのオブジェクト

        Returns:
            bool: データの登録が成功したら真を返す

        """
        items = [
            "site_name",
            "postal_code",
            "address",
            "phone_number",
            "latitude",
            "longitude",
            "updated_at",
        ]

        column_names = ""
        place_holders = ""
        upsert = ""
        for item in items:
            column_names += "," + item
            place_holders += ",%s"
            upsert += "," + item + "=%s"

        state = (
            "INSERT INTO"
            + " "
            + self.__table_name
            + " "
            + "("
            + column_names[1:]
            + ")"
            + " "
            + "VALUES ("
            + place_holders[1:]
            + ")"
            + " "
            "ON CONFLICT(latitude,longitude)" + " "
            "DO UPDATE SET" + " " + upsert[1:]
        )

        values = [
            evacuation_site.site_name,
            evacuation_site.postal_code,
            evacuation_site.address,
            evacuation_site.phone_number,
            evacuation_site.latitude,
            evacuation_site.longitude,
            datetime.now(timezone(timedelta(hours=+9))),
        ]
        # UPDATE句用に登録データ配列を重複させる
        values += values

        try:
            self.__db.execute(state, values)
            return True
        except (DatabaseError, DataError) as e:
            self.__logger.error_log(e.args[0])
            return False
