from bson import ObjectId
from src.infra.database import Database
from src.common.models.user_models import User, UserDB

class UserRepository:
    def __init__(self):
        database = Database()
        collection = database.client.trash_cash.users
        self.collection = collection

    async def create_user(self, user:UserDB):
        try:
            user_json = user.dict()
            user_json.pop("id")
            await self.collection.insert_one(user_json)
        except Exception as ex:
            print(ex)
            raise ex
        
    async def get_user_by_id(self, id:str)->dict|None:
        try:
            result = await self.collection.find({"_id":ObjectId(id)}).to_list(None)
            return result[0]
        except:
            return None

    async def get_user_by_email(self, email:str)->UserDB|None:
        try:
            user = await self.collection.find({"email":email}).to_list(None)
            if user == [] or user == None:
                return None 
            return user[0]
        except:
            return None

    async def update_user_data(self, user:UserDB)->bool:
        user_dict = user.dict()
        user_dict.pop("id")
        result = await self.collection.update_one({"_id":user.id}, {'$set':user_dict})
        if result.modified_count != 0:
            return True
        return False
    
    async def deactivate_user_by_id(self, user:User) -> bool:
        user.disabled = True
        return await self.update_user_data(user)
        
