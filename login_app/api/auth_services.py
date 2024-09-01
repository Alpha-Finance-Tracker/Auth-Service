import os
from typing import Annotated

import bcrypt
from fastapi import status
from jose import jwt, JWTError
from dotenv import load_dotenv

from login_app.database import read_query, update_query
from login_app.utils.responses import NotFound, Unauthorized, EmailExists
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

ACCESS_TOKEN_EXPIRATION = 15
REFRESH_TOKEN_EXPIRATION = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')

logged_users = {}


async def login_user(email: str, password: str):
    user = await authenticate_user(email, password)

    access_token = await create_access_token(user[0][0])

    refresh_token = await create_refresh_token(user[0][0])

    logged_users.update({f"{user[0][0]}": {'Email': email}})

    return {
        "access_token": access_token,
        'refresh_token': refresh_token,
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
    info = await read_query('SELECT * FROM users WHERE email = %s', (email,))
    if info:
        raise EmailExists()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    await update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (email, hashed_password))
    return {"message": "User registered successfully!"}


async def create_access_token(user_id):
    user = await read_query('SELECT user_id,email,role FROM users WHERE user_id = %s', (user_id,))
    expiration = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)

    data_to_encode = {'user_id': user[0][0], 'email': user[0][1], 'role': user[0][2], 'exp': expiration}
    encode_jwt = jwt.encode(data_to_encode, secret_key, algorithm)
    print(encode_jwt)
    return encode_jwt


async def create_refresh_token(user_id):
    expiration = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRATION)
    data = {'user_id': user_id, 'exp': expiration}

    return jwt.encode(data, secret_key, algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
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


async def refresh_access_token_service(token):
    refresh_token = await verify_refresh_token_service(token)
    access_token = await create_access_token(refresh_token['user_id'])

    return {'token': access_token, 'Validity': refresh_token['Validity']}  # The validity of the refresh token


async def refresh_refresh_token_service(token):
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    refresh_token = await create_refresh_token(payload.get('user_id'))

    return refresh_token


async def verify_access_token_service(token):
    if not token:
        raise Unauthorized

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        exp_time = datetime.fromtimestamp(payload.get('exp'))
        if exp_time > datetime.now():
            return token
    except JWTError:
        raise Unauthorized


async def verify_refresh_token_service(token):
    if not token:
        raise Unauthorized

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        exp_time = datetime.fromtimestamp(payload.get('exp'))
        time_remaining = exp_time - datetime.now()
        if time_remaining.total_seconds() > 172800:  # 2 days in seconds
            return {'Validity': 'Valid', 'token': token, 'user_id': payload.get('user_id')}
        else:
            return {'Validity': 'Expires', 'token': token, 'user_id': payload.get('user_id')}
    except JWTError:
        raise Unauthorized


async def authenticate_user(email: str, password: str):
    user_info = await read_query('SELECT * FROM users WHERE email = %s', (email,))

    if not user_info:
        raise NotFound

    if bcrypt.checkpw(password.encode('utf-8'), user_info[0][2].encode('utf-8')):
        return user_info
    else:
        raise NotFound
