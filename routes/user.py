from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.university_model import University
from .auth import get_current_user
from app.models.user_model import User
from app.models.career_model import CareerPath
from app.models.program_model import Program
from app.models.university_program_model import UniversityProgram
from app.database import get_db  # Function to get the database session

router = APIRouter()

# GET /user/profile/{username} - Retrieve user profile information by username
@router.get("/profile/{username}")
def get_user_profile_by_username(username: str, db: Session = Depends(get_db)):
    # Query the database for the user by username
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the user profile information
    return {
        "id": user.id,
        "username": user.username,
        "baccalaureate_score": user.baccalaureate_score,
        "baccalaureate_section": user.baccalaureate_section,
        "career_path_id": user.career_path_id,
    }

# GET /user/career_path - Fetch general career path suggestions 
@router.get("/user/career_path")
def get_career_path_suggestions(
    baccalaureate_section: str,
    baccalaureate_score: float,
    db: Session = Depends(get_db)
):
    career_paths = db.query(CareerPath).all()
    if not career_paths:
        raise HTTPException(status_code=404, detail="No career paths found.")
    
    return {"message": "Career path suggestions fetched successfully", "career_paths": career_paths}

# GET /user/university_programs - Retrieves university programs based on the user's career path and baccalaureate score.
@router.get("/user/university_programs")
def get_university_programs(
    baccalaureate_section: str,
    baccalaureate_score: float,
    db: Session = Depends(get_db)
):
    # Construct the section field dynamically
    section_field = f"min_score_{baccalaureate_section.lower()}"

    # Query the database with the necessary joins
    programs = (
        db.query(
            UniversityProgram.id,
            University.name.label("university_name"),
            University.location.label("university_location"),
            Program.program_name.label("program_name"),
            UniversityProgram.min_score_science,
            UniversityProgram.min_score_maths,
            UniversityProgram.min_score_economics,
            UniversityProgram.min_score_literature,
            UniversityProgram.min_score_info
        )
        .join(University, UniversityProgram.university_id == University.id)  # Join Universities table
        .join(Program, UniversityProgram.program_id == Program.program_id)     # Join Programs table
        .filter(getattr(UniversityProgram, section_field) <= baccalaureate_score)  # Filter by baccalaureate score
        .all()
    )

    # Check if programs exist
    if not programs:
        raise HTTPException(status_code=404, detail="No eligible university programs found.")
    
    # Structure the response
    formatted_programs = [
        {
            "id": program.id,
            "university_name": program.university_name,
            "university_location": program.university_location,
            "program_name": program.program_name,
            "min_score_science": program.min_score_science,
            "min_score_maths": program.min_score_maths,
            "min_score_economics": program.min_score_economics,
            "min_score_literature": program.min_score_literature,
            "min_score_info": program.min_score_info
        }
        for program in programs
    ]

    return {
        "message": "Eligible university programs fetched successfully",
        "programs": formatted_programs
    }

# GET /users - Fetch all users with their scores, sections, and desired career paths
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    try:
        # Query users with their career path details
        users = (
            db.query(
                User.id.label("user_id"),
                User.username,
                User.baccalaureate_score,
                User.baccalaureate_section,
                CareerPath.general_field.label("career_path_general"),
                CareerPath.specific_career_path.label("career_path_specific"),
            )
            .outerjoin(CareerPath, User.career_path_id == CareerPath.id) 
            .all()
        )
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found in the database.")

        user_list = [
            {
                "user_id": user.user_id,
                "username": user.username,
                "baccalaureate_score": user.baccalaureate_score,
                "baccalaureate_section": user.baccalaureate_section,
                "career_path_general": user.career_path_general,
                "career_path_specific": user.career_path_specific,
            }
            for user in users
        ]

        return {
            "message": "Users fetched successfully.",
            "users": user_list,
        }
    except Exception as e:
        # Log the error for debugging
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# PUT /user/preferences - Updates the user's career path based on their username
@router.put("/user/preferences")
def update_user_career_path(
    username: str, 
    career_path_id: int,
    db: Session = Depends(get_db),
):
    # Retrieve the user by username
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    career_path = db.query(CareerPath).filter(CareerPath.id == career_path_id).first()
    if not career_path:
        raise HTTPException(status_code=404, detail="Career path not found.")

    # Update the user's career path
    user.career_path_id = career_path_id
    db.commit()
    db.refresh(user)

    return {
        "message": "Career path updated successfully.",
        "username": username,
        "career_path_id": career_path_id,
    }

