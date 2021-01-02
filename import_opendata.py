from hinanbasho.db import DB
from hinanbasho.errors import DatabaseError, DataError
from hinanbasho.models import EvacuationSiteFactory
from hinanbasho.services import EvacuationSiteService
from hinanbasho.scraper import Scraper


def import_opendata():
    """データベースに旭川市オープンデータの避難場所データを格納"""

    # Webサイトからデータを抽出する処理
    scraped_data = Scraper()
    factory = EvacuationSiteFactory()
    for row in scraped_data.lists:
        factory.create(row)

    # 抽出データをデータベースへ格納する処理
    db = DB()
    try:
        service = EvacuationSiteService(db)
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
