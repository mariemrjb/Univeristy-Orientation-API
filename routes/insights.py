from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.insights_model import Insight
from app.models.career_model import CareerPath

router = APIRouter()

# GET /insights/employability - Get employability rates by career field
@router.get("/employability")
def get_employability_rates(db: Session = Depends(get_db)):
    insights = db.query(Insight).all()
    if not insights:
        raise HTTPException(status_code=404, detail="No employability data found")

    employability_rates = [
        {
            "career_path_id": insight.career_path_id,
            "career_path": db.query(CareerPath).filter(CareerPath.id == insight.career_path_id).first().specific_career_path,
            "employability_rate": insight.employability_rate,
        }
        for insight in insights
    ]
    return {"employability_rates": employability_rates}

# GET /insights/salaries - Get average salaries by career field
@router.get("/salaries")
def get_average_salaries(db: Session = Depends(get_db)):
    insights = db.query(Insight).all()
    if not insights:
        raise HTTPException(status_code=404, detail="No salary data found")

    average_salaries = [
        {
            "career_path_id": insight.career_path_id,
            "career_path": db.query(CareerPath).filter(CareerPath.id == insight.career_path_id).first().specific_career_path,
            "average_salary": insight.average_salary,
        }
        for insight in insights
    ]
    return {"average_salaries": average_salaries}

# GET /insights/career-path/{career_path_id} - Get employability and salary insights for a career path
@router.get("/{career_path_id}")
def get_employability_and_salary(career_path_id: int, db: Session = Depends(get_db)):
    insights = db.query(Insight).filter(Insight.career_path_id == career_path_id).first()
    
    if not insights:
        raise HTTPException(status_code=404, detail="No insights found for the specified career path.")

    career_path = db.query(CareerPath).filter(CareerPath.id == career_path_id).first()
    
    if not career_path:
        raise HTTPException(status_code=404, detail="Career path not found.")

    return {
        "career_path_id": career_path_id,
        "career_path_name": career_path.specific_career_path,  # Include the name of the career path
        "employability_rate": insights.employability_rate,
        "average_salary": insights.average_salary,
    }