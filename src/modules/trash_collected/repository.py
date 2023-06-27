from fastapi.encoders import jsonable_encoder
from src.common.models.trash_collected import TrashCollected
from src.infra.database import Database

def _get_trash_collected():
    database = Database()
    collection = database.client.trash_cash.trash_collected
    return collection

async def create_trash_collected(trashCollected:TrashCollected):
    collection = _get_trash_collected()
    try:
        trash_collected_json = jsonable_encoder(trashCollected)
        await collection.insert_one(trash_collected_json)
        return True
    except Exception as e:
        print(e)
        return False

async def read_trash_collected(collection_point:str|None = None, id:str|None = None):
    collection = _get_trash_collected()
    try:
        query = {}
        if collection_point!=None and collection_point!="":
            query["collection_point"] = collection_point
        if id!=None and id!="":
            query["_id"]=id
        result = await collection.find(query).to_list(None)
        return result
    except Exception as e:
        print(e)
        return False

async def update_trash_collected(updated_trash_collected:TrashCollected):
    collection = _get_trash_collected()
    try:
        id = str(updated_trash_collected.id)
        trash_collected_dict = updated_trash_collected.dict()
        trash_collected_dict.pop("id", None)
        result = await collection.update_one({'_id': id}, {'$set': trash_collected_dict})
        if result.modified_count != 0:
            return True
        return False
    except Exception as e:
        print(e)
        return False

async def delete_trash_collected(id:str):
    collection = _get_trash_collected()
    try:
        result = await collection.delete_one({"_id":id})
        return result
    except Exception as e:
        print(e)
        return False