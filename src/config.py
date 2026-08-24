import os

from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


DATA_DIR = "dados"

SCHEMA_STAGING = "stg_enem"

ANOS = [2019, 2020, 2021, 2022, 2023]