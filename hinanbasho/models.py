from hinanbasho.factory import Factory


class EvacuationSite:
    """避難場所のデータモデル

    Attributes:
        name (str): 避難場所名
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
        self.__name = str(kwargs["name"])
        self.__postal_code = str(kwargs["postal_code"])
        self.__address = str(kwargs["address"])
        self.__phone_number = str(kwargs["phone_number"])
        self.__latitude = float(kwargs["latitude"])
        self.__longitude = float(kwargs["longitude"])

    @property
    def name(self) -> str:
        return self.__name

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
