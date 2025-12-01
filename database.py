from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


INIT_ENGINE = create_engine("mysql+pymysql://root:Program_Coffee_123@localhost", isolation_level="AUTOCOMMIT")

with INIT_ENGINE.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS StockData"))

DATABASE_URL = "mysql+pymysql://root:Program_Coffee_123@localhost/StockData"
engine = create_engine(DATABASE_URL, echo=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()