from fastapi import Form
from pydantic import BaseModel

class OAuth2EmailRequestForm:
    def __init__(
        self,
        email: str = Form(...),
        password: str = Form(...),
    ):
        self.email = email
        self.password = password

class Token(BaseModel):
    access_token: str
    token_type: str