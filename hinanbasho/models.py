from decimal import ROUND_HALF_UP, Decimal

import numpy as np

from hinanbasho.errors import LocationError
from hinanbasho.factory import Factory


class Point:
    """
    緯度と経度を要素に持つ地点情報を表す。

    Attributes:
        latitude (float): 緯度（北緯）を表す小数
        longitude (float): 経度（東経）を表す小数

    """

    def __init__(self, latitude: float, longitude: float):
        """
        Args:
            latitude (float): 緯度（北緯）を表す小数
            longitude (float): 経度（東経）を表す小数

        """
        try:
            self.__latitude = float(latitude)
            self.__longitude = float(longitude)
        except (TypeError, ValueError):
            raise LocationError("緯度経度の値が正しくありません。")

    @property
    def latitude(self) -> float:
        return self.__latitude

    @property
    def longitude(self) -> float:
        return self.__longitude


class EvacuationSite(Point):
    """避難場所のデータモデル

    Attributes:
        site_id (int): 連番
        site_name (str): 避難場所名
        postal_code (str): 避難場所の郵便番号
        address (str): 避難場所の住所
        phone_number (str): 避難場所の電話番号
        latitude (float): 避難場所の緯度
        longitude (float): 避難場所の経度

    """

    def __init__(
        self,
        site_id: int,
        site_name: str,
        postal_code: str,
        address: str,
        phone_number: str,
        latitude: float,
        longitude: float,
    ):
        """
        Args:
            site_id (int): 連番
            site_name (str): 避難場所名
            postal_code (str): 避難場所の郵便番号
            address (str): 避難場所の住所
            phone_number (str): 避難場所の電話番号
            latitude (float): 避難場所の緯度
            longitude (float): 避難場所の経度

        """
        self.__site_id = int(site_id)
        self.__site_name = str(site_name)
        self.__postal_code = str(postal_code)
        self.__address = str(address)
        self.__phone_number = str(phone_number)
        Point.__init__(self, float(latitude), float(longitude))

    @property
    def site_id(self) -> int:
        return self.__site_id

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

    def _create_item(self, **row: dict) -> EvacuationSite:
        """避難場所オブジェクトを作成する。

        Args:
            row (dict): 避難場所情報を表すディクショナリ

        """
        return EvacuationSite(**row)

    def _register_item(self, item: EvacuationSite) -> None:
        """避難場所オブジェクトをリストに追加。

        Args:
            item (:obj:`EvacuationSite`): 避難場所オブジェクト

        Returns:
            bool: 成功したら真を返す

        """
        self.__items.append(item)


class CurrentLocation(Point):
    """
    現在地の情報を表す

    Attributes:
        latitude (float): 避難場所の緯度
        longitude (float): 避難場所の経度

    """

    def __init__(self, latitude: float = None, longitude: float = None):
        Point.__init__(self, latitude, longitude)

    def get_distance_to(self, end_point: Point) -> float:
        """
        現在地と避難場所の2点間の距離を計算して返す。

        Args:
            end_point (obj:`Point`): 避難場所の緯度と経度を持つオブジェクト

        Returns:
            distance (float): 現在地と避難場所の2点間の距離（メートル）

        """
        earth_radius = 6378137.00
        start_latitude = np.radians(self.latitude)
        start_longitude = np.radians(self.longitude)
        end_latitude = np.radians(end_point.latitude)
        end_longitude = np.radians(end_point.longitude)
        distance = earth_radius * np.arccos(
            np.sin(start_latitude) * np.sin(end_latitude)
            + np.cos(start_latitude)
            * np.cos(end_latitude)
            * np.cos(end_longitude - start_longitude)
        )
        return float(
            Decimal(str(distance)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )


class AreaAddress:
    """町域と郵便番号のデータモデル

    Attributes:
        postal_code (str): 郵便番号
        area_name (str): 町域名

    """

    def __init__(
        self,
        postal_code: str,
        area_name: str,
    ):
        """
        Args:
            postal_code (str): 郵便番号
            area_name (str): 町域名

        """
        postal_code = str(postal_code)
        postal_code = postal_code[:3] + "-" + postal_code[-4:]
        self.__postal_code = postal_code
        self.__area_name = str(area_name)

    @property
    def postal_code(self) -> str:
        return self.__postal_code

    @property
    def area_name(self) -> str:
        return self.__area_name


class AreaAddressFactory(Factory):
    """町域と郵便番号モデルを作成する。

    Attributes:
        items (list of :obj:`AreaAddress`): 町域と郵便番号オブジェクトのリスト

    """

    def __init__(self):
        self.__items = list()

    @property
    def items(self) -> list:
        return self.__items

    def _create_item(self, **row: dict) -> AreaAddress:
        """町域と郵便番号オブジェクトを作成する。

        Args:
            row (dict): 町域と郵便番号情報を表すディクショナリ

        """
        return AreaAddress(**row)

    def _register_item(self, item: AreaAddress) -> None:
        """町域と郵便番号オブジェクトをリストに追加。

        Args:
            item (:obj:`AreaAddress`): 町域と郵便番号オブジェクト

        Returns:
            bool: 成功したら真を返す

        """
        self.__items.append(item)
