from fastapi import APIRouter
from src.modules.collection_points.repository import create_collection_point, read_collection_points, update_collection_point, delete_collection_point
from src.common.models.collection_point import CollectionPoint

collection_points_router = APIRouter(tags=["Collection Points"])

@collection_points_router.post("/create")
async def create_collection_point_controller(collection_point: CollectionPoint):
    result = await create_collection_point(collection_point)
    if result:
        return 201
    return 400

@collection_points_router.get("/read", response_model=list[CollectionPoint])
async def read_collection_point_controller(address:str|None = None, id:str|None = None):
    result =  await read_collection_points(address,id)
    return result

@collection_points_router.patch("/update")
async def update_collection_point_controller(updated_collection_point: CollectionPoint):
    result = await update_collection_point(updated_collection_point)
    if result:
        return 201
    return 400

@collection_points_router.delete("/delete/{id}")
async def delete_collection_point_controller(id:str):
    await delete_collection_point(id)
    return 202