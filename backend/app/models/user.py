from sqlalchemy import Column, String, Numeric
from app.core.database import Base

class User(Base):
    __tablename__ = "user"
    name = Column(String(50), primary_key=True, index=True)
    city_name = Column(String(100), nullable=False)