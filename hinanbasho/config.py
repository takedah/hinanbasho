import os


class Config:
    DATABASE_URL = os.environ.get("HINANBASHO_DB_URL")
