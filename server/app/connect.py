import os
import time
import logging
from urllib.parse import urlparse
import psycopg2
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def wait_for_db(db_url, max_retries=10, wait_time=1):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    result = urlparse(db_url)
    dbname = result.path[1:]
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    retries = 0

    logger.info(f"Trying to connect to {host}:{port} as {user}...")

    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.close()
            logger.info("Connection successful!")
            return
        except Exception as e:
            logger.warning(f"Postgres is not ready yet. Waiting... {str(e)}")
            time.sleep(wait_time)
            retries += 1

    logger.error("Max retries reached. Unable to connect to the database.")


DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL:", DATABASE_URL)

wait_for_db(DATABASE_URL)

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_db_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with async_db_session() as session:
        yield session
