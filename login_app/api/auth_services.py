import os
import bcrypt
from typing import Annotated
from starlette import status
from jose import jwt, JWTError
from dotenv import load_dotenv
from utils.responses import NotFound
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.query_services import authenticate_user_service, login_service, register_service, \
    check_if_email_is_already_registered



TOKEN_EXPIRATION = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()

logged_users = {}

async def authenticate_user(email:str, password:str):
    user = authenticate_user_service(email)

    return  None if not authenticate_user_service(email) else bcrypt.checkpw(password.encode('utf-8'), user[0][1].encode('utf-8'))


async def login_user(email:str, password:str):
    if authenticate_user(email,password) is None:
        raise NotFound

    user =  login_service(email)

    token = await generate_token({'user_id':user[0][0],
                            'email':user[0][1],
                            'role':user[0][3]})

    logged_users.update({f"{user[0][0]}":{'Email':email}})

    return {
        "access_token":token,
        "token_type":"bearer",
        "role":user[0][2]
    }

async def logout_user(user):
    id = user.get("id")
    if logged_users[str(id)]:
        logged_users.popitem()
        return {'message': 'Successfully logged out.'}
    else:
        raise NotFound



async def register_user(email:str, password:str):
    registered = await check_if_email_is_already_registered(email)
    return {"message":'Email already registered'} if registered == True else register_service(email,password)


async def generate_token(data: dict):
    data_to_encode = data.copy() # Shallow copy to avoid modifying the original
    expiration =datetime.now() + timedelta(minutes=TOKEN_EXPIRATION)
    data_to_encode.update({'exp': expiration, 'last_activity': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")})


    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    encode_jwt = jwt.encode(data_to_encode, secret_key,algorithm)

    return encode_jwt


async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
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

