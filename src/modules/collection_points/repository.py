from fastapi.encoders import jsonable_encoder
from src.common.models.collection_point import CollectionPoint
from src.infra.database import Database

def _get_updated_collection_point_collections():
    database = Database()
    collection = database.client.trash_cash.collection_point
    return collection

async def create_collection_point(collection_point:CollectionPoint):
    collection = _get_updated_collection_point_collections()
    try:
        collection_point_json = jsonable_encoder(collection_point)
        await collection.insert_one(collection_point_json)
        return True
    except Exception as e:
        print(e)
        return False

async def read_collection_points(address:str|None = None, id:str|None = None):
    collection = _get_updated_collection_point_collections()
    try:
        query = {}
        if address!=None and address!="":
            query["address"] = address
        if id!=None and id!="":
            query["_id"] = id
        result = await collection.find(query).to_list(None)
        return result
    except Exception as e:
        print(e)
        return False

async def update_collection_point(updated_collection_point:CollectionPoint):
    collection = _get_updated_collection_point_collections()
    try:
        id = str(updated_collection_point.id)
        collection_point_dict = updated_collection_point.dict()
        collection_point_dict.pop("id", None)
        result = await collection.update_one({'_id': id}, {'$set': collection_point_dict})
        if result.modified_count != 0:
            return True
        return False
    except Exception as e:
        print(e)
        return False

async def delete_collection_point(id:str):
    collection = _get_updated_collection_point_collections()
    try:
        result = await collection.delete_one({"_id":id})
        return result
    except Exception as e:
        print(e)
        return False