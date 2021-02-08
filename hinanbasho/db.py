import psycopg2
from psycopg2.extras import DictCursor

from hinanbasho.config import Config
from hinanbasho.errors import DatabaseError, DataError


class DB:
    """PostgreSQLデータベースの操作を行う。

    Attributes:
        conn (:obj:`psycopg2.connection`): PostgreSQL接続クラス。

    """

    def __init__(self):
        try:
            self.__conn = psycopg2.connect(Config.DATABASE_URL)
            self.__cursor = self.__conn.cursor(cursor_factory=DictCursor)
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
            raise DatabaseError(e.args[0])

    def execute(self, sql, parameters=None) -> bool:
        """cursorオブジェクトのexecuteメソッドのラッパー。

        Args:
            sql (str): SQL文
            parameters (tuple): SQLにプレースホルダを使用する場合の値を格納したリスト

        Returns:
            bool: 成功したら真を返す。

        """
        try:
            if parameters:
                self.__cursor.execute(sql, parameters)
            else:
                self.__cursor.execute(sql)
            return True
        except (
            psycopg2.DataError,
            psycopg2.IntegrityError,
            psycopg2.InternalError,
        ) as e:
            raise DataError(e.args[0])

    def fetchall(self) -> psycopg2.extras.DictCursor:
        """cursorオブジェクトのfetchallメソッドのラッパー。

        Returns:
            results (:obj:`psycopg2.extras.DictCursor`): 検索結果のイテレータ

        """
        return self.__cursor.fetchall()

    def commit(self) -> bool:
        """PostgreSQLデータベースにクエリをコミットする。

        Returns:
            bool: 成功したら真を返す。

        """
        self.__conn.commit()
        return True

    def rollback(self) -> bool:
        """PostgreSQLデータベースのクエリをロールバックする。

        Returns:
           bool: 成功したら真を返す。

        """
        self.__conn.rollback()
        return True

    def close(self) -> bool:
        """PostgreSQLデータベースへの接続を閉じる。
        Returns:
           bool: 成功したら真を返す。

        """
        self.__conn.close()
        return True
