from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./grocery_store.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, default="")
    price = Column(Float, nullable=False)
    category = Column(String, default="Other")
    unit = Column(String, default="piece")
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)
