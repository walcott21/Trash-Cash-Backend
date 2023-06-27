from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from src.common.models.base.py_object_id import PyObjectId

class Claim(BaseModel):
    user_id:str = Field(...)
    date:str = Field(...)

class Reward(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name:str = Field(...)
    claims:Optional[list[Claim]] = Field([])
    image:str = Field(...)
    value:int = Field(...)
    quantity:int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}


