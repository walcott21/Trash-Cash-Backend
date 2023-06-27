from bson import ObjectId
from pydantic import BaseModel, Field
from src.common.models.base.py_object_id import PyObjectId


class TrashCollected(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type:list[str] = Field([])
    weight:float = Field(...)
    user_id:str = Field(...)
    collection_point_id:str = Field(...)
    date:str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}
