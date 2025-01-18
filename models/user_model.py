from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    baccalaureate_score = Column(Float, nullable=True)
    baccalaureate_section = Column(String, nullable=True)
    career_path_id = Column(Integer, ForeignKey("careerpaths.id"), nullable=True)

    career_path = relationship("CareerPath", back_populates="users")