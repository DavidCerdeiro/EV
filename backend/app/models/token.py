from sqlalchemy import Column, String, Text
from app.core.database import Base

class AppToken(Base):
    __tablename__ = "app_token"
    application = Column(String(50), primary_key=True, index=True)
    token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)