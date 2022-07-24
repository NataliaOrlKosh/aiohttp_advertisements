import os


user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")


PG_DSN = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
