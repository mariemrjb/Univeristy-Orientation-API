from fastapi import FastAPI
from app.database import Base, engine
from app.models import user_model, career_model, program_model, university_model, university_program_model  # Import the models
from app.routes import user, auth, universities, programs, insights, university_program

# Create the FastAPI app
app = FastAPI(
    title="University Orientation API",
    description="An API to explore career paths, programs, and universities.",
    version="1.0.0",
)


# Include your routers
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(universities.router, prefix="/universities", tags=["Universities"])
app.include_router(programs.router, prefix="/programs", tags=["Programs"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(university_program.router, prefix="/university-programs", tags=["University Programs"])