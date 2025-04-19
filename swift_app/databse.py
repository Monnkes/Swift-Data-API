from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from swift_app.settings import config
from swift_app.utils.data_loader import load_initial_data


engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()
