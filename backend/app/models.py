# app/models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    pdf_path = Column(String, nullable=False)

# Database setup
DATABASE_URL = "sqlite:///../business.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def add_business(name: str, category: str, file_path: str):
    db: Session = SessionLocal()
    new_business = Business(name=name, type=category, pdf_path=file_path)
    db.add(new_business)
    db.commit()
    db.close()

def get_businesses():
    db: Session = SessionLocal()
    businesses = db.query(Business).all()
    db.close()
    return [
        {
            "id": b.id,
            "name": b.name,
            "type": b.type,
            "pdf_path": b.pdf_path
        } for b in businesses
    ]
