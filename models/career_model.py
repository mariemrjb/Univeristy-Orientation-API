from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.database import Base

class CareerPath(Base):
    __tablename__ = "careerpaths"

    id = Column(Integer, primary_key=True, index=True)
    general_field = Column(String, index=True)
    specific_career_path = Column(String, nullable=True)

    users = relationship("User", back_populates="career_path")
    programs = relationship("Program", back_populates="career_path")
    insights = relationship("Insight", back_populates="career_path")