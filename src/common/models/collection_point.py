from bson import ObjectId
from pydantic import BaseModel, Field
from src.common.models.base.py_object_id import PyObjectId


class CollectionPoint(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    address:str = Field(...)
    type_of_trash:list[str] = Field([])

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = False
        json_encoders = {ObjectId: str}