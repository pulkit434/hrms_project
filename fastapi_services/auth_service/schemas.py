# from pydantic import BaseModel, EmailStr
# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str

# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: EmailStr
#     class Config:
#         orm_mode = True

# class UserUpdate(BaseModel):
#     username: str
#     email: EmailStr

from pydantic import BaseModel, EmailStr

# Base schema for shared user fields (optional, useful for inheritance)
class UserBase(BaseModel):
    username: str
    email: EmailStr

#  Used during registration (includes password)
class UserCreate(UserBase):
    password: str

#  Used for reading user responses (e.g., from the DB)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # This is required to work with SQLAlchemy models

#  Used when updating user info (no password here)
class UserUpdate(UserBase):
    pass
