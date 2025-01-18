from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.university_model import University as UniversityModel
from app.schemas.university_schema import University, UniversityCreate, UniversityUpdate
from app.models.university_program_model import UniversityProgram
from app.models.program_model import Program


router = APIRouter()

# GET /universities - Fetches a list of all universities
@router.get("/")
def get_all_universities(db: Session = Depends(get_db)):
    universities = db.query(UniversityModel).all()  
    if not universities:
        raise HTTPException(status_code=404, detail="No universities found.")
    return {"universities": universities}

# GET /universities/{university_id}: Fetches a specific university by its id.
@router.get("/{university_id}", response_model=University)
def read_university(university_id: int, db: Session = Depends(get_db)):
    db_university = db.query(UniversityModel).filter(UniversityModel.id == university_id).first()
    if db_university is None:
        raise HTTPException(status_code=404, detail="University not found")
    return db_university

# POST /universities - Add a new university to the database
@router.post("/", response_model=University)
def create_university(university: UniversityCreate, db: Session = Depends(get_db)):
    db_university = UniversityModel(**university.dict())
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university

# PUT /universities/{university_id} - Updates a university's information (name, location, and type).
@router.put("/{university_id}", response_model=University)
def update_university(university_id: int, university: UniversityUpdate, db: Session = Depends(get_db)):
    db_university = db.query(UniversityModel).filter(UniversityModel.id == university_id).first()
    if db_university is None:
        raise HTTPException(status_code=404, detail="University not found")
    for key, value in university.dict().items():
        setattr(db_university, key, value)
    db.commit()
    db.refresh(db_university)
    return db_university

#GET /universities/{university_id}/programs - Retrieves all programs offered by a specific university using the UniversityProgram junction table.
@router.get("/{university_id}/programs")
def get_programs_by_university(university_id: int, db: Session = Depends(get_db)):
    
    university_programs = (
        db.query(UniversityProgram)
        .filter(UniversityProgram.university_id == university_id)
        .all()
    )

    if not university_programs:
        raise HTTPException(status_code=404, detail=f"No programs found for university ID {university_id}.")

    university = db.query(UniversityModel).filter(UniversityModel.id == university_id).first()  # Use UniversityModel
    if not university:
        raise HTTPException(status_code=404, detail=f"University with ID {university_id} not found.")

    programs = []
    for up in university_programs:
        
        program = db.query(Program).filter(Program.program_id == up.program_id).first()
        
        if program:
          
            programs.append({
                "program_id": program.program_id,
                "program_name": program.program_name,  
                "min_score_science": up.min_score_science,
                "min_score_maths": up.min_score_maths,
                "min_score_literature": up.min_score_literature,
                "min_score_economics": up.min_score_economics,
                "min_score_info": up.min_score_info,
            })

    response = {
        "university_id": university.id,
        "university_name": university.name,  
        "programs": programs
    }

    return response

# POST /universities/{university_id}/programs/{program_id} - Adds a program to a university
@router.post("/{university_id}/programs/{program_id}")
def add_program_to_university(
    university_id: int,
    program_id: int,
    min_score_science: float = None,
    min_score_maths: float = None,
    min_score_literature: float = None,
    min_score_economics: float = None,
    min_score_info: float = None,
    db: Session = Depends(get_db),
):
    
    university = db.query(UniversityModel).filter(UniversityModel.id == university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found.")

    program = db.query(Program).filter(Program.program_id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found.")

    existing_entry = db.query(UniversityProgram).filter(
        UniversityProgram.university_id == university_id,
        UniversityProgram.program_id == program_id,
    ).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="This program is already linked to the university.")

    # Add the relationship to the junction table
    new_entry = UniversityProgram(
        university_id=university_id,
        program_id=program_id,
        min_score_science=min_score_science,
        min_score_maths=min_score_maths,
        min_score_literature=min_score_literature,
        min_score_economics=min_score_economics,
        min_score_info=min_score_info,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Program successfully added to university.",
        "entry": {
            "university_id": new_entry.university_id,
            "program_id": new_entry.program_id,
            "min_score_science": new_entry.min_score_science,
            "min_score_maths": new_entry.min_score_maths,
            "min_score_literature": new_entry.min_score_literature,
            "min_score_economics": new_entry.min_score_economics,
            "min_score_info": new_entry.min_score_info,
        }
    }

# DELETE /universities/{university_id}/programs/{program_id} - Deletes a program to a university
@router.delete("/{university_id}/programs/{program_id}")
def delete_program_from_university(
    university_id: int,
    program_id: int,
    db: Session = Depends(get_db),
):
    # Check if the relationship exists
    existing_entry = db.query(UniversityProgram).filter(
        UniversityProgram.university_id == university_id,
        UniversityProgram.program_id == program_id,
    ).first()
    
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Program not linked to this university.")

    # Delete the relationship from the junction table
    db.delete(existing_entry)
    db.commit()

    return {
        "message": "Program successfully removed from university.",
        "entry": {
            "university_id": university_id,
            "program_id": program_id,
        }
    }


# DELETE /universities/{university_id} - Delete a university.
@router.delete("/{university_id}", response_model=University)
def delete_university(university_id: int, db: Session = Depends(get_db)):
    db_university = db.query(UniversityModel).filter(UniversityModel.id == university_id).first()
    if db_university is None:
        raise HTTPException(status_code=404, detail="University not found")
    db.delete(db_university)
    db.commit()
    return db_university