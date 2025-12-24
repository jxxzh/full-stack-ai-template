from app.core.db import SessionLocal, init_db
from app.core.logger import logger


def main() -> None:
    logger.info("Creating initial data")
    with SessionLocal() as session:
        init_db(session)
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
