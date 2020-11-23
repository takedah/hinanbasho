from datetime import datetime
from datetime import timedelta
from datetime import timezone
from hinanbasho.db import DatabaseError
from hinanbasho.db import DataError
from hinanbasho.models import EvacuationSite
from hinanbasho.logs import DBLog


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
        """避難場所テーブルのデータを全削除"""
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
