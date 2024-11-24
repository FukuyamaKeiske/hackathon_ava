from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TextRequest(BaseModel):
    user_id: str
    text: str

class BusinessRegister(BaseModel):
    user_id: str
    name: str
    sphere: str
    size: str
    type: str
    specialization: str
