import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Aiven Connection String
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://avnadmin:YOUR_PWD@YOUR_HOST:23622/defaultdb?sslmode=require")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True, index=True)
    fund_name = Column(String, nullable=False)
    amfi_code = Column(String, nullable=False) # Critical for mftool lookup
    category = Column(String)
    investment_date = Column(Date, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    units_held = Column(Numeric(12, 4)) # Added for accurate valuation
    status = Column(String, default="ACTIVE")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()