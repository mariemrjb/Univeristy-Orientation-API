from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.university_program_model import UniversityProgram
from app.models.university_model import University
from app.models.program_model import Program
from app.database import get_db

router = APIRouter()

# GET /university-programs -retrieve all university programs
@router.get("/")
def get_all_university_programs(db: Session = Depends(get_db)):
    university_programs = (
        db.query(UniversityProgram)
        .join(University, UniversityProgram.university_id == University.id)
        .join(Program, UniversityProgram.program_id == Program.program_id)
        .all()
    )
    
    if not university_programs:
        raise HTTPException(status_code=404, detail="No university-programs found")

    university_programs = [
        {
            "university_id": up.university_id,
            "university_name": db.query(University).filter(University.id == up.university_id).first().name,
            "program_id": up.program_id,
            "program_name": db.query(Program).filter(Program.program_id == up.program_id).first().program_name,
            "min_score_science": up.min_score_science,
            "min_score_maths": up.min_score_maths,
            "min_score_literature": up.min_score_literature,
            "min_score_economics": up.min_score_economics,
            "min_score_info": up.min_score_info,
        }
        for up in university_programs
    ]

    return {"university_programs": university_programs}

# GET /university-programs/university/{university_id} - Retrieve programs by university
@router.get("/university/{university_id}")
def get_programs_by_university(university_id: int, db: Session = Depends(get_db)):
    university_programs = db.query(UniversityProgram).filter(UniversityProgram.university_id == university_id).all()
    if not university_programs:
        raise HTTPException(status_code=404, detail="No programs found for this university")
    return {"programs": university_programs}

# GET /university-programs/program/{program_id} - Retrieve universities by program
@router.get("/program/{program_id}")
def get_universities_by_program(program_id: int, db: Session = Depends(get_db)):
    university_programs = db.query(UniversityProgram).filter(UniversityProgram.program_id == program_id).all()
    if not university_programs:
        raise HTTPException(status_code=404, detail="No universities found offering this program")
    return {"universities": university_programs}

# GET /university-programs/eligibility - Check eligibility based on student score
@router.get("/eligibility")
def check_eligibility(
    student_score: float,
    student_section: str,
    program_id: int,
    university_id: int,
    db: Session = Depends(get_db)
):
    university_program = db.query(UniversityProgram).filter(
        UniversityProgram.university_id == university_id,
        UniversityProgram.program_id == program_id
    ).first()

    if not university_program:
        raise HTTPException(status_code=404, detail="University or Program not found")

    # Determine the minimum score based on the student's section
    section_min_score_map = {
        "science": university_program.min_score_science,
        "maths": university_program.min_score_maths,
        "literature": university_program.min_score_literature,
        "economics": university_program.min_score_economics,
        "info": university_program.min_score_info,
    }

    if student_section not in section_min_score_map:
        raise HTTPException(status_code=400, detail="Invalid baccalaureate section")

    min_score = section_min_score_map[student_section]

    # Check eligibility (handle NULL or no score requirement for private universities)
    if min_score is None or student_score >= min_score:
        return {"eligibility": True, "message": "The student is eligible for this program at the university."}
    else:
        return {"eligibility": False, "message": "The student does not meet the minimum score requirement."}
