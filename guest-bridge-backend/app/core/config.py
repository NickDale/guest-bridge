import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    VENDEGEM_USER = 'vendegem.sync@gmail.com'
    VENDEGEM_SECRET = 'C$3kkpoint0x0'


settings = Settings()
