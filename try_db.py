from src.config import DbConfig
from src.db.connection import DataBaseConnection

with DataBaseConnection(DbConfig.from_env()) as db:
    with db.cursor() as cur:
        cur.execute("SELECT 1 AS x")
        print(cur.fetchall())
