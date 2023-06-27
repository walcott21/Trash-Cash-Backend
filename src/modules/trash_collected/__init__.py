from fastapi import APIRouter
from src.modules.trash_collected.repository import create_trash_collected, read_trash_collected, update_trash_collected, delete_trash_collected
from src.common.models.trash_collected import TrashCollected

trash_collected_router = APIRouter(tags=["Trash Collected"])

@trash_collected_router.post("/create")
async def create_trash_collected_controller(trashCollected: TrashCollected):
    result = await create_trash_collected(trashCollected)
    if result:
        return 201
    return 400

@trash_collected_router.get("/read", response_model=list[TrashCollected])
async def read_trash_collected_controller(collection_point:str|None = None,id:str|None = None):
    result =  await read_trash_collected(collection_point,id)
    return result

@trash_collected_router.patch("/update")
async def update_trash_collected_controller(updated_trash_collected: TrashCollected):
    result = await update_trash_collected(updated_trash_collected)
    if result:
        return 201
    return 400

@trash_collected_router.delete("/delete/{id}")
async def delete_trash_collected_controller(id:str):
    await delete_trash_collected(id)
    return 202