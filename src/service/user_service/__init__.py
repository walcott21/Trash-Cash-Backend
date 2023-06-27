
from src.service.user_service.user_repository import UserRepository
from src.common.models.exception_models import DuplicatedUser, IncorrectLogin
from src.common.models.user_models import CreateUser, User, UserAuth, UserDB
from src.infra.auth.auth_service import AuthService

class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.auth_service = AuthService()

    async def create_user(self, new_user:CreateUser):
        already_exist = await self.get_user_by_email(new_user.email)
        if already_exist!=None:
            if already_exist.disabled:
                await self.__activate_user(already_exist, new_user.password)
            else:
                raise DuplicatedUser("User already exist")
        else:
            await self.__save_new_user(new_user)
        user_auth = await self.validate_login(new_user.email,new_user.password)
        return user_auth

    async def update_user(self, user:CreateUser) -> User|None:
        try:
            user_db = UserDB(**user.dict(),hashed_password=self.auth_service.hash_password(user.password))
            is_updated = await self.repository.update_user_data(user_db)
            if is_updated:
                return user
            else:
                return None
        except Exception as er:
            print(er)
            raise er
        
    async def deactivate_user(self, user:User) -> bool:
        try:
            return await self.repository.deactivate_user_by_id(user)
        except Exception as er:
            print(er)
            raise er

    async def get_user_by_id(self,user_id:str)-> User|None:
        try:
            user_dict = await self.repository.get_user_by_id(user_id)
            if user_dict:
                return User(**user_dict)
        except Exception as er:
            print(er)
            return None

    async def get_user_by_email(self, user_email:str):
        user_dict = await self.repository.get_user_by_email(user_email)
        if user_dict:
            user_db = UserDB.parse_obj(user_dict)
            return user_db
        else:
            return None

    async def validate_login(self, user_email:str, password:str)-> UserAuth:
        user_db = await self.get_user_by_email(user_email)
        if user_db == None:
            raise IncorrectLogin()
        if self.auth_service.verify_password(password, user_db.hashed_password):
            token = self.auth_service.create_bearer_token(user_db.id,{})
            return UserAuth(**user_db.__dict__ ,token_type="bearer",access_token=token)
        else:
            raise IncorrectLogin()
        
    async def __activate_user(self,already_exist:UserDB, new_password )->bool:
        user = CreateUser(**(already_exist.dict()),password=new_password)
        hashed_password = self.auth_service.hash_password(new_password)
        user.password = hashed_password
        user.disabled = False
        await self.update_user(User(**(user.dict())))

    async def __save_new_user(self,new_user:CreateUser):
        hashed_password = self.auth_service.hash_password(new_user.password)
        user_db = UserDB(**new_user.__dict__,hashed_password=hashed_password)
        await self.repository.create_user(user_db)