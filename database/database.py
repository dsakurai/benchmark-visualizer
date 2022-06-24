from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import sql_engine_url

engine = create_engine(sql_engine_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
