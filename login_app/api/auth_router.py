from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm,HTTPBearer, HTTPAuthorizationCredentials

from login_app.api.auth_services import get_current_user, register_user, login_user, logout_user, \
    refresh_access_token_service, refresh_refresh_token_service, verify_access_token

user_dependency = Annotated[dict,Depends(get_current_user)]
security = HTTPBearer()
auth_router = APIRouter(prefix='')


@auth_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_user(form_data.username, form_data.password)

@auth_router.post('/register')
async def register(email: str, password: str):
    return await register_user(email, password)

@auth_router.post('/logout')
async def logout(user:user_dependency):
    return await logout_user(user)

@auth_router.get('/refresh_access_token')
async def refresh_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await refresh_access_token_service(credentials.credentials)

@auth_router.get('/refresh_refresh_token')
async def refresh_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await refresh_refresh_token_service(credentials.credentials)

@auth_router.get('/verify_access_token')
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await verify_access_token(credentials.credentials)
