import os


class Config:
    DATABASE_URL = os.environ.get("HINANBASHO_DB_URL")
    OPENDATA_URL = (
        "https://www.city.asahikawa.hokkaido.jp/kurashi/320/321/d053843_d/fil/"
        + "012041_hinanbasho_list.csv"
    )
    POST_OFFICE_CSV_PATH = "hinanbasho/data/01HOKKAI.CSV"
