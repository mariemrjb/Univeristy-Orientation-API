from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, nullable=True)
    type = Column(String, nullable=True)

     # Define the relationship
    university_program = relationship("UniversityProgram", back_populates="university")


