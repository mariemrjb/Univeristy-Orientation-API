from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Program(Base):
    __tablename__ = "programs"

    program_id = Column(Integer, primary_key=True, index=True)
    program_type = Column(String(100), nullable=False)
    program_name = Column(String(100), nullable=False)
    career_path_id = Column(Integer, ForeignKey("careerpaths.id"), nullable=False)

    # Relationship through the junction table 'UniversityProgram'
    university_program = relationship("UniversityProgram", back_populates="program")
    career_path = relationship("CareerPath")