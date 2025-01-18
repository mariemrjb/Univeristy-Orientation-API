from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Insight(Base):
    __tablename__ = "Insights"

    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("careerpaths.id"), nullable=False)
    employability_rate = Column(Float, nullable=True)
    average_salary = Column(Float, nullable=True)

    career_path = relationship("CareerPath", back_populates="insights")