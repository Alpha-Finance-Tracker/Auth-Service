from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from login_app.api.services.auth_service import AuthService
from login_app.api.services.token_service import TokenService

# Initialize HTTP Bearer security scheme
security = HTTPBearer()
# Create a router for authentication-related endpoints
auth_router = APIRouter(prefix='')


@auth_router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Handles user login by validating credentials.

    Parameters:
        form_data (OAuth2PasswordRequestForm): A form containing the username (email) and password.

    Returns:
        dict: A dictionary containing:
            - "access_token": The access token for the session.
            - "refresh_token": The refresh token for the session.
            - "token_type": The type of the token, typically "bearer".

        Raises:
            HTTPException: If authentication fails.
    """
    return await AuthService(email=form_data.username, password=form_data.password).login()


@auth_router.post('/register')
async def register(email: str, password: str):
    """
    Handles new user registration.

    Parameters:
        email (str): The email address for the new user.
        password (str): The password for the new user.

    Returns:
        dict: A message signaling successful registration.

        Raises:
            HTTPException: If registration fails.
    """
    return await AuthService(email=email, password=password).register()


@auth_router.get('/refresh_access_token')
async def refresh_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refreshes the access token using a valid refresh token.

    Parameters:
        credentials (HTTPAuthorizationCredentials): Bearer token from the Authorization header.

    Returns:
        dict: A dictionary containing:
            - "access_token": The new access token.
            - "expires_in": The duration (in seconds) for which the token is valid.

        Raises:
            HTTPException: If the refresh token is invalid or expired.
    """
    return await TokenService(token=credentials.credentials).refresh_access_token()


@auth_router.get('/refresh_refresh_token')
async def refresh_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Refreshes the refresh token using a valid refresh token.

    Parameters:
        credentials (HTTPAuthorizationCredentials): Bearer token from the Authorization header.

    Returns:
        dict: A dictionary containing:
            - "refresh_token": The new refresh token.

        Raises:
            HTTPException: If the refresh token is invalid or expired.
    """
    return await TokenService(token=credentials.credentials).refresh_refresh_token()


@auth_router.get('/verify_access_token')
async def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifies the validity of an access token.

    Parameters:
        credentials (HTTPAuthorizationCredentials): Bearer token from the Authorization header.

    Returns:
        dict: A dictionary containing:
            - "is_valid": Boolean indicating if the token is valid.
            - "user_id": The ID of the user associated with the token.

        Raises:
            HTTPException: If the access token is invalid or expired.
    """
    return await TokenService(token=credentials.credentials).verify_access_token()


@auth_router.get('/verify_refresh_token')
async def verify_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifies the validity of a refresh token.

    Parameters:
        credentials (HTTPAuthorizationCredentials): Bearer token from the Authorization header.

    Returns:
        dict: A dictionary containing:
            - "is_valid": Boolean indicating if the token is valid.
            - "user_id": The ID of the user associated with the token.

        Raises:
            HTTPException: If the refresh token is invalid or expired.
    """
    return await TokenService(token=credentials.credentials).verify_refresh_token()
