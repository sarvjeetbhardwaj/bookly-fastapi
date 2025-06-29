from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.create_engine import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService
#from src.db.redis import token_in_blocklist
from src.auth.models import User
from typing import List
from src.errors import InvalidToken, RefreshTokenRequired, AccessTokenRequired, InsufficientPermission, AccountNotVerified

user_service = UserService()

class TokenBearer(HTTPBearer):
    """
                By default, if the HTTP Bearer token is not provided (in an
                `Authorization` header), `HTTPBearer` will automatically cancel the
                request and send the client an error.

                If `auto_error` is set to `False`, when the HTTP Bearer token
                is not available, instead of erroring out, the dependency result will
                be `None`.

                This is useful when you want to have optional authentication.

                It is also useful when you want to have authentication that can be
                provided in one of multiple optional ways (for example, in an HTTP
                Bearer token or in a cookie).
    """
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds =  await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token=token)

        if not self.token_valid(token=token):
            raise InvalidToken ()
        #if await token_in_blocklist(token_data['jti']):
        #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error' : 'This token is invalid or has been revoked',
        #                                                                       'resolution' : 'Please get new token'})
        
        #self.verify_token_data(token_data=token_data)
        
        return token_data

    def token_valid(self, token:str) -> bool:
        token_data = decode_token(token=token)

        if token_data  is not None:
            return True
        else:
            return False
        
    def verify_token_data(self, token_data):
        raise NotImplementedError('Please Override this method in child classes')
        

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenBearer()
        
async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), 
                           session: AsyncSession = Depends(get_session)):
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(email=user_email, session=session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str] ):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):

        if not current_user.is_verified:
            raise AccountNotVerified()

        if current_user.role in self.allowed_roles:
            return True
        
        raise InsufficientPermission()
    
