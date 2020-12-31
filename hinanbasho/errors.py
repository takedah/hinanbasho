class Error(Exception):
    pass


class LocationError(Error):
    """地点情報オブジェクトを作成できない時に生じるエラー

    Attributes:
        message (str): エラーメッセージ

    """

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message


class DatabaseError(Error):
    """データベース接続に関するエラー

    Attributes:
        message (str): エラーメッセージ

    """

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message


class DataError(Error):
    """SQL実行に関するエラー

    Attributes:
        message (str): エラーメッセージ

    """

    def __init__(self, message):
        self.__message = message

    @property
    def message(self):
        return self.__message
