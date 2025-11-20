from pydantic import BaseModel , EmailStr
class User(BaseModel):
    name:str
    age:int
    email:EmailStr
    password:str

class UpdateUser(BaseModel):
    name:str
    age:int
    email:EmailStr

class Login(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    age:int
    email:EmailStr

class DeleteResponse(BaseModel):
    message: str
    user_id: int