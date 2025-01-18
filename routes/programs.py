from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.program_model import Program
from app.models.career_model import CareerPath
from app.models.university_program_model import UniversityProgram
from app.database import get_db

router = APIRouter()

# POST /programs - Add a new program to the database
@router.post("/programs")
def create_program(
    program_name: str,
    program_type: str,  
    career_path_id: int,  
    db: Session = Depends(get_db),
):
    # Check if the career path exists
    career_path = db.query(CareerPath).filter(CareerPath.id == career_path_id).first()
    if not career_path:
        raise HTTPException(status_code=404, detail=f"Career path with id {career_path_id} not found")

    # Create a new program with the provided program_type and career_path_id
    new_program = Program(
        program_name=program_name,
        program_type=program_type,  
        career_path_id=career_path_id  
    )
    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return {"message": "Program created successfully", "program": new_program}

# GET /programs - Retrieve all programs in the database
@router.get("/programs")
def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    if not programs:
        raise HTTPException(status_code=404, detail="No programs found")
    return {"programs": programs}

# GET /programs/{program_id} - Retrieve a specific program by ID
@router.get("/{program_id}")
def get_program_by_id(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return {"program": program}

# GET /programs/career-path/{career_path_id} - Retrieve programs based on a specific career path
@router.get("/career-path/{career_path_id}")
def get_programs_by_career_path(career_path_id: int, db: Session = Depends(get_db)):
    
    programs = db.query(Program).join(UniversityProgram).join(CareerPath).filter(CareerPath.id == career_path_id).all()
    if not programs:
        raise HTTPException(status_code=404, detail="No programs found for this career path")
    return {"programs": programs}

# DELETE /programs/{program_id} - Delete a specific program by ID
@router.delete("/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found.")
    
    db.delete(program)
    db.commit()

    return {
        "message": "Program successfully deleted.",
        "program_id": program_id,
    }