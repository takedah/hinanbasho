import numpy as np
from decimal import Decimal
from decimal import ROUND_HALF_UP
from hinanbasho.factory import Factory


class Point:
    """
    地点の情報を表す。

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
        self.__latitude = float(latitude)
        self.__longitude = float(longitude)

    @property
    def latitude(self) -> float:
        return self.__latitude

    @property
    def longitude(self) -> float:
        return self.__longitude


class EvacuationSite(Point):
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
        Point.__init__(self, float(kwargs["latitude"]), float(kwargs["longitude"]))

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


class CurrentLocation(Point):
    """
    現在地の情報を表す

    Attributes:
        latitude (float): 避難場所の緯度
        longitude (float): 避難場所の経度

    """

    def __init__(self, latitude: float = 0, longitude: float = 0):
        Point.__init__(self, latitude, longitude)

    def get_distance_to(self, end_point: EvacuationSite) -> float:
        """
        避難場所の緯度と経度を属性に持つオブジェクトを引数に取り、
        現在地と避難場所の2点間の距離を計算して返す。

        Args:
            end_point (obj:`EvacuationSite`): 避難場所の緯度と経度を持つオブジェクト

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
