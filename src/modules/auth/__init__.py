
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.service.user_service import UserService
from src.service.user_service.middlewares import auth_middleware
from src.common.models.exception_models import DuplicatedUser, IncorrectLogin
from src.common.models.user_models import CreateUser, User, UserAuth
from src.infra.auth.auth_service import AuthService

auth_service = AuthService()
user_service = UserService()
auth_router = APIRouter()
user_router = APIRouter(tags=["User"])

@auth_router.post("/login", response_model=UserAuth)
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    try:
        user_authenticated = await user_service.validate_login(form_data.username, form_data.password)
        return user_authenticated
    except IncorrectLogin as e:
        message = "Incorrect username or password. "
        if len(e.args)>0:
            message += str(e.args[0])
        raise HTTPException(status_code=401,detail=message)
    except Exception as er:
        print(er)
        raise HTTPException(status_code=500, detail="Something Wrong here")
    
@auth_router.post("/signup")
async def create_user(new_user:CreateUser):
    try:
        return await user_service.create_user(new_user)
    except DuplicatedUser:
        raise HTTPException(status_code=400, detail="Duplicated user Email")

@auth_router.get("/getuser", response_model=User)
async def get_test(user: User = Depends(auth_middleware)):
    user = await user_service.get_user_by_id(user.id)
    if user.disabled:
        raise HTTPException(status_code=400, detail="This user is disabled")
    return user

@user_router.get("/{id}")
async def get_user(id: str):
    user = await user_service.get_user_by_id(id)
    if user: 
        if user.disabled:
            raise HTTPException(status_code=400, detail="This user is disabled")
        return user
    return 400

@auth_router.patch("/update_user", response_model=User)
async def update_user(new_user_data:CreateUser, user: User = Depends(auth_middleware)):
    user_updated = await user_service.update_user(new_user_data)
    if user_updated == None:
        raise HTTPException(status_code=400, detail="User Not Updated")
    return user_updated

@auth_router.delete("/delete",response_model=bool)
async def delete_user(user: User = Depends(auth_middleware)):
    result = await user_service.deactivate_user(user)
    return result