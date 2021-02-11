from hinanbasho.db import DB
from hinanbasho.errors import DatabaseError, DataError
from hinanbasho.models import EvacuationSiteFactory
from hinanbasho.scraper import OpenData
from hinanbasho.services import EvacuationSiteService


def import_opendata():
    """データベースに旭川市オープンデータの避難場所データを格納"""

    open_data = OpenData()
    factory = EvacuationSiteFactory()
    for row in open_data.lists:
        factory.create(**row)

    db = DB()
    try:
        service = EvacuationSiteService(db)
        service.truncate()
        for evacuation_site in factory.items:
            service.create(evacuation_site)
        db.commit()
    except (DatabaseError, DataError) as e:
        db.rollback()
        print(e.message)
    finally:
        db.close()


if __name__ == "__main__":
    import_opendata()
