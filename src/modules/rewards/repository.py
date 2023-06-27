from fastapi.encoders import jsonable_encoder
from src.common.models.rewards import Reward
from src.infra.database import Database

def _get_reward_collections():
    database = Database()
    collection = database.client.trash_cash.rewards
    return collection

async def create_reward(reward:Reward):
    collection = _get_reward_collections()
    try:
        reward_json = jsonable_encoder(reward)
        await collection.insert_one(reward_json)
        return True
    except Exception as e:
        print(e)
        return False

async def read_rewards(name:str|None = None, id:str|None = None):
    collection = _get_reward_collections()
    try:
        query = {}
        if name!=None and name!="":
            query = {"name":name}
        if id!=None and id!="":
            query = {"_id":id}
        result = await collection.find(query).to_list(None)
        return result
    except Exception as e:
        print(e)
        return False

async def update_reward(updated_reward:Reward):
    collection = _get_reward_collections()
    try:
        id = str(updated_reward.id)
        reward_dict = updated_reward.dict()
        reward_dict.pop("id", None)
        result = await collection.update_one({'_id': id}, {'$set': reward_dict})
        if result.modified_count != 0:
            return True
        return False
    except Exception as e:
        print(e)
        return False

async def delete_reward(id:str):
    collection = _get_reward_collections()
    try:
        result = await collection.delete_one({"_id":id})
        return result
    except Exception as e:
        print(e)
        return False