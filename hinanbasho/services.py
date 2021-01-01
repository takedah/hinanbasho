from datetime import datetime
from datetime import timedelta
from datetime import timezone
from hinanbasho.errors import DatabaseError
from hinanbasho.errors import DataError
from hinanbasho.models import CurrentLocation
from hinanbasho.models import EvacuationSite
from hinanbasho.models import EvacuationSiteFactory
from hinanbasho.logs import DBLog


class EvacuationSiteService:
    """避難場所サービス"""

    def __init__(self, db):
        self.__db = db
        self.__table_name = "evacuation_sites"
        self.__logger = DBLog()

    def truncate(self) -> bool:
        """避難場所テーブルのデータを全削除

        Returns:
            bool: データの登録が成功したら真を返す

        """
        state = "TRUNCATE TABLE " + self.__table_name + " RESTART IDENTITY;"
        try:
            self.__db.execute(state)
            return True
        except (DatabaseError, DataError) as e:
            self.__logger.error_log(e.message)
            return False

    def create(self, evacuation_site: EvacuationSite) -> bool:
        """データベースへ避難場所データを保存

        Args:
            evacuation_site (obj:`EvacuationSite`): 避難場所データのオブジェクト

        Returns:
            bool: データの登録が成功したら真を返す

        """
        items = [
            "site_id",
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
            "ON CONFLICT(site_id)" + " "
            "DO UPDATE SET" + " " + upsert[1:]
        )

        values = [
            evacuation_site.site_id,
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
            self.__logger.error_log(e.message)
            return False

    def get_all(self) -> list:
        """条件に合致する避難場所データのリストを返す。

        Returns:
            sites (list of obj:`EvacuationSiteFactory`): 避難場所オブジェクト全件のリスト

        """
        state = (
            "SELECT site_id,site_name,postal_code,address,phone_number,latitude,longitude"
            + " "
            + "FROM evacuation_sites ORDER BY id;"
        )
        self.__db.execute(state)
        factory = EvacuationSiteFactory()
        for row in self.__db.fetchall():
            factory.create(row)
        return factory.items

    def get_near_sites(self, current_location: CurrentLocation) -> list:
        """
        現在地から直線距離で最も近い避難場所上位5件の避難場所データのリストを返す。

        Args:
            current_location (obj:`CurrentLocation`): 現在地の緯度経度情報を持つ
                オブジェクト

        Returns:
            near_sites (list of dicts): 現在地から最も近い避難場所上位5件の
                避難場所オブジェクトと現在地までの距離のリストを要素に持つ二次元配列

        """
        near_sites = list()
        for site in self.get_all():
            near_sites.append(
                {
                    "site": site,
                    "distance": current_location.get_distance_to(site),
                }
            )
        return sorted(near_sites, key=lambda x: x["distance"])[:5]
