import os
from typing import Annotated
from starlette import status
from jose import jwt, JWTError
from dotenv import load_dotenv
from login_app.utils.responses import NotFound
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from login_app.utils.query_services import register_service, authenticate_user

TOKEN_EXPIRATION = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()

logged_users = {}


async def login_user(email: str, password: str):
    user = await authenticate_user(email, password)

    token = await create_access_token({'user_id': user[0][0],
                                  'email': user[0][1],
                                  'role': user[0][3]})

    logged_users.update({f"{user[0][0]}": {'Email': email}})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user[0][2]
    }


async def logout_user(user):
    user_id = user.get("id")
    if logged_users[str(user_id)]:
        logged_users.popitem()
        return {'message': 'Successfully logged out.'}
    else:
        raise NotFound


async def register_user(email: str, password: str):
    return await register_service(email,password)



async def create_access_token(data: dict):
    data_to_encode = data.copy()  # Shallow copy to avoid modifying the original
    expiration = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    data_to_encode.update({'exp': expiration, 'last_activity': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")})
    print(data_to_encode['exp'])

    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    encode_jwt = jwt.encode(data_to_encode, secret_key, algorithm)
    return encode_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        secret_key = os.getenv('SECRET_KEY')
        algorithm = os.getenv('ALGORITHM')
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email = payload.get('email')
        user_id = payload.get('user_id')
        role = payload.get('role')

        if email is None or user_id is None:
            raise credentials_exception

        user_data = {
            "email": email,
            "id": user_id,
            "role": role
        }

        return user_data

    except JWTError:
        raise credentials_exception


async def decode_token(token):
    try:
        secret_key = os.getenv('SECRET_KEY')
        algorithm = os.getenv('ALGORITHM')
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except Exception as e:
        print(f"Error decoding JWT: {e}")

async def refresh_token(token):

    decoded_payload = await decode_token(token)
    if decoded_payload:
        return  await create_access_token(decoded_payload)
    else:
        raise ValueError("Invalid token")
