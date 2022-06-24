from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    mail: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class ConstructionTreeBase(BaseModel):
    tree_data: bytes
    created_time: datetime


class ConstructionTree(ConstructionTreeBase):
    tree_id: int
    # user_id: int

    class Config:
        orm_mode = True


class JsonGraph(BaseModel):
    vertices: list[dict]
    edges: list[dict]
