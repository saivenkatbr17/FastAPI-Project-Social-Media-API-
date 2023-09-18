from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Lahari.2007@localhost/API_Development'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

