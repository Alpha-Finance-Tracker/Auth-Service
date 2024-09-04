from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm,HTTPBearer, HTTPAuthorizationCredentials
from login_app.api.services.auth_service import AuthService
from login_app.api.services.token_service import TokenService


security = HTTPBearer()
auth_router = APIRouter(prefix='')


@auth_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
   return await AuthService(email=form_data.username,password=form_data.password).login()

@auth_router.post('/register')
async def register(email: str, password: str):
    return await AuthService(email=email,password=password).register()

@auth_router.get('/refresh_access_token')
async def refresh_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await TokenService(token=credentials.credentials).refresh_access_token()

@auth_router.get('/refresh_refresh_token')
async def refresh_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await TokenService(token=credentials.credentials).refresh_refresh_token()

@auth_router.get('/verify_access_token')
async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await TokenService(token=credentials.credentials).verify_access_token()

@auth_router.get('/verify_refresh_token')
async def verify_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return await TokenService(token=credentials.credentials).verify_refresh_token()
