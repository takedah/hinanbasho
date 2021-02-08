from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal

from hinanbasho.errors import DatabaseError, DataError
from hinanbasho.models import (
    AreaAddress,
    CurrentLocation,
    EvacuationSite,
    EvacuationSiteFactory
)


class EvacuationSiteService:
    """避難場所サービス"""

    def __init__(self, db):
        """
        Args:
            db (obj:`DB`): psycopg2のメソッドをラップしたメソッドを持つオブジェクト

        """
        self.__db = db
        self.__table_name = "evacuation_sites"

    def truncate(self) -> bool:
        """避難場所テーブルのデータを全削除

        Returns:
            bool: データの登録が成功したら真を返す

        """
        state = "TRUNCATE TABLE " + self.__table_name + " RESTART IDENTITY;"
        try:
            self.__db.execute(state)
            return True
        except (DatabaseError, DataError):
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
        except (DatabaseError, DataError):
            return False

    def _fetch(self, dict_cursor) -> list:
        """
        psycopg2.extras.DictCursorオブジェクトから避難場所データのリストを作成する。

        Args:
            dict_cursor (obj:`psycopg2.extras.DictCursor`): 検索結果のイテレータ

        Returns:
            sites (list of obj:`EvacuationSite`): 検索結果の避難場所オブジェクトのリスト

        """
        factory = EvacuationSiteFactory()
        for row in dict_cursor:
            factory.create(row)
        return factory.items

    def get_all(self) -> list:
        """避難場所全件データのリストを返す。

        Returns:
            sites (list of obj:`EvacuationSite`): 避難場所オブジェクト全件のリスト

        """
        state = (
            "SELECT site_id,site_name,postal_code,address,phone_number,latitude,"
            + "longitude FROM evacuation_sites ORDER BY site_id;"
        )
        self.__db.execute(state)
        return self._fetch(self.__db.fetchall())

    def get_near_sites(self, current_location: CurrentLocation) -> list:
        """
        現在地から直線距離で最も近い避難場所上位5件の避難場所データのリストを返す。

        Args:
            current_location (obj:`CurrentLocation`): 現在地の緯度経度情報を持つ
                オブジェクト

        Returns:
            near_sites (list of dicts): 現在地から最も近い避難場所上位5件の
                避難場所オブジェクトと現在地までの距離のリストを要素に持つ辞書のリスト

        """
        near_sites = list()
        for site in self.get_all():
            near_sites.append(
                {
                    "order": None,
                    "site": site,
                    "distance": current_location.get_distance_to(site),
                }
            )
        near_sites = sorted(near_sites, key=lambda x: x["distance"])[:5]
        for i in range(len(near_sites)):
            # 現在地から近い順で連番を付与する。
            near_sites[i]["order"] = i + 1
            # 距離を分かりやすくするためキロメートルに変換する。
            near_sites[i]["distance"] = float(
                Decimal(str(near_sites[i]["distance"] / 1000)).quantize(
                    Decimal("0.1"), rounding=ROUND_HALF_UP
                )
            )
        return near_sites

    def find_by_site_id(self, site_id) -> list:
        """
        避難場所連番から該当する避難場所データを返す。

        Args:
            site_id (int): 避難場所連番

        Returns
            evacuation_site (list of obj:`EvacuationSite`): 避難場所データ

        """
        state = (
            "SELECT site_id,site_name,postal_code,address,phone_number,latitude,"
            + "longitude FROM evacuation_sites WHERE site_id=%s;"
        )
        self.__db.execute(state, (str(site_id),))
        return self._fetch(self.__db.fetchall())

    def get_area_names(self) -> list:
        """
        避難場所の住所の町域一覧を返す。

        Returns:
            area_names (list): 避難場所の住所の町域のリスト

        """
        state = (
            "SELECT DISTINCT ON (area_name) area_name FROM evacuation_sites "
            + "LEFT JOIN area_addresses ON evacuation_sites.postal_code="
            + "area_addresses.postal_code;"
        )
        area_names = list()
        self.__db.execute(state)
        for row in self.__db.fetchall():
            area_names.append(row["area_name"])
        return area_names

    def find_by_area_name(self, area_name) -> list:
        """
        町域名から避難場所を検索する。

        Args:
            area_name (str): 町域名

        Returns:
            area_sites (list of dicts): 指定した町域名を含む町域の避難場所の
                避難場所オブジェクトのリスト

        """
        state = (
            "SELECT site_id,site_name,evacuation_sites.postal_code,address,"
            + "phone_number,latitude,longitude,area_name FROM evacuation_sites "
            + "LEFT JOIN area_addresses ON evacuation_sites.postal_code="
            + "area_addresses.postal_code WHERE area_name=%s;"
        )
        self.__db.execute(state, (area_name,))
        return self._fetch(self.__db.fetchall())

    def find_by_site_name(self, site_name) -> list:
        """
        指定した避難場所名を含む避難場所を検索する。

        Args:
            site_name (int): 避難場所名（キーワード）

        Returns
            evacuation_site (list of obj:`EvacuationSite`): 避難場所データ

        """
        site_name = "%" + site_name + "%"
        state = (
            "SELECT site_id,site_name,postal_code,address,phone_number,latitude,"
            + "longitude FROM evacuation_sites WHERE site_name LIKE %s;"
        )
        self.__db.execute(state, (site_name,))
        return self._fetch(self.__db.fetchall())


class AreaAddressService:
    """町域と郵便番号サービス"""

    def __init__(self, db):
        """
        Args:
            db (obj:`DB`): psycopg2のメソッドをラップしたメソッドを持つオブジェクト

        """
        self.__db = db
        self.__table_name = "area_addresses"

    def truncate(self) -> bool:
        """町域と郵便番号テーブルのデータを全削除

        Returns:
            bool: データの登録が成功したら真を返す

        """
        state = "TRUNCATE TABLE " + self.__table_name + " RESTART IDENTITY;"
        try:
            self.__db.execute(state)
            return True
        except (DatabaseError, DataError):
            return False

    def create(self, area_address: AreaAddress) -> bool:
        """データベースへ町域と郵便番号データを保存

        Args:
            area_address (obj:`AreaAddress`): 町域と郵便番号データのオブジェクト

        Returns:
            bool: データの登録が成功したら真を返す

        """
        items = [
            "postal_code",
            "area_name",
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
            "ON CONFLICT(postal_code)" + " "
            "DO UPDATE SET" + " " + upsert[1:]
        )

        values = [
            area_address.postal_code,
            area_address.area_name,
            datetime.now(timezone(timedelta(hours=+9))),
        ]
        # UPDATE句用に登録データ配列を重複させる
        values += values

        try:
            self.__db.execute(state, values)
            return True
        except (DatabaseError, DataError):
            return False
