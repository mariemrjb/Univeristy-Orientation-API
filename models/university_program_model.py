from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UniversityProgram(Base):
    __tablename__ = "UniversityPrograms"

    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id", ondelete="CASCADE"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.program_id", ondelete="CASCADE"), nullable=False)
    
    # Minimum scores for each baccalaureate section
    min_score_science = Column(Float, nullable=True)  # NULL for no min score (e.g., private universities)
    min_score_maths = Column(Float, nullable=True)
    min_score_literature = Column(Float, nullable=True)
    min_score_economics = Column(Float, nullable=True)
    min_score_info = Column(Float, nullable=True)

    # Relationships
    university = relationship("University", back_populates="university_program")
    program = relationship("Program", back_populates="university_program")