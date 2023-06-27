from bson import ObjectId
from pydantic import BaseModel, Field
from src.common.models.base.py_object_id import PyObjectId

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str = Field(...)
    name: str = Field(...)
    disabled: bool|None = Field(False)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}

class CreateUser(User):
    password:str = Field(...)

class UserAuth(User):
    access_token:str = Field(...)
    token_type:str = Field(...)

class UserDB(User):
    hashed_password:str = Field(...)