from hinanbasho.db import DB
from hinanbasho.errors import DatabaseError, DataError
from hinanbasho.models import AreaAddressFactory
from hinanbasho.scraper import PostOfficeCSV
from hinanbasho.services import AreaAddressService


def import_post_office_csv():
    """データベースに日本郵便Webサイトの郵便番号CSVデータを格納"""

    post_office_csv = PostOfficeCSV()
    factory = AreaAddressFactory()
    for row in post_office_csv.lists:
        factory.create(**row)

    db = DB()
    try:
        service = AreaAddressService(db)
        for area_address in factory.items:
            service.create(area_address)
        db.commit()
    except (DatabaseError, DataError) as e:
        db.rollback()
        print(e.message)
    finally:
        db.close()


if __name__ == "__main__":
    import_post_office_csv()
