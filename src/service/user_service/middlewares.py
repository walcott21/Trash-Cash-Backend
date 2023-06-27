from fastapi import Depends
from jose import JWSError, jwt
from src.common.models.token_payload import TokenPayload
from src.common.models.exception_models import Unauthorized
from src.infra.auth.auth_service import AuthService
from src.service.user_service import UserService

auth_service = AuthService()
user_service = UserService()

async def auth_middleware(token:str = Depends(auth_service.o_auth2_password_bearer)):
    try:
        if token == None:
            raise Unauthorized()
        payload = jwt.decode(token,key=auth_service.SECRET_KEY,algorithms=auth_service.ALGORITHM)
        token_payload = TokenPayload(**payload)
        return await user_service.get_user_by_id(token_payload.sub)
    except JWSError as jwt_err:
        print(jwt_err)
        raise Unauthorized()