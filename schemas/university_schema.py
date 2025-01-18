from pydantic import BaseModel

class UniversityBase(BaseModel):
    name: str
    location: str

class UniversityCreate(UniversityBase):
    pass

class UniversityUpdate(UniversityBase):
    pass

class University(UniversityBase):
    id: int

    class Config:
        orm_mode: True