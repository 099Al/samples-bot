import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

TOKEN_ID = os.getenv('TOKEN_ID')
SUPER_ADMIN_ID = os.getenv('SUPER_ADMIN_ID')
BOT_ID = os.getenv('BOT_ID')

# db_config = {
#     'HOST': os.getenv('DB_HOST'),
#     'USER': os.getenv('DB_USER'),
#     'PASS': os.getenv('DB_PASSWORD'),
#     'DB_NAME': os.getenv('DB_NAME')
# }
class Settings(BaseSettings):
    HOST: str | None = None
    PORT: str | None = None
    USER: str | None = None
    PASS: str | None = None
    DB: str | None = None
    ENGINE: str | None = None
    SQL_DB: str | None = None

    path_env: str = str(Path(__file__).resolve().parent)
    model_config = SettingsConfigDict(enf_file=f"{path_env}/.env")
    @property
    def connect_url(self):
        if self.SQL_DB:
            return self.SQL_DB
        else:
            return f'{self.ENGINE}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}'
            # return f'mysql+aiomysql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}?charset=utf8mb4'
            # return 'sqlite:///db.sqlite3'   # for alembic
            # return 'sqlite:///shop2.db'
            #return 'sqlite+aiosqlite:///db.sqlite3'  #for aiogram
            #return r'sqlite+aiosqlite:///D:/WorkSpaces/PythonWs/shop/db.sqlite3'  # for TEST

    def _url(self):
        return f'{self.ENGINE}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}'
        # return f'mysql+aiomysql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.DB}?charset=utf8mb4'
        # return 'sqlite:///db.sqlite3'   # for alembic
        # return 'sqlite:///shop2.db'
        # return 'sqlite+aiosqlite:///db.sqlite3'  #for aiogram
        # return r'sqlite+aiosqlite:///D:/WorkSpaces/PythonWs/shop/db.sqlite3'  # for TEST

settings = Settings()




