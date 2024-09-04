import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt, JWTError

from login_app.database import read_query
from login_app.models.base_models.token import Token
from login_app.utils.responses import Unauthorized

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


class AccessToken(Token):
    ACCESS_TOKEN_EXPIRATION = 15  # Min

    def __init__(self, token, user_id):
        self.token = token
        self.expiration = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRATION)
        self.user_id = user_id

    async def encode(self, data):
        try:
            return jwt.encode(data, secret_key, algorithm)
        except Exception as e:
            raise e

    async def decode(self):
        try:
            return jwt.decode(self.token, secret_key, algorithms=[algorithm])
        except Exception as e:
            raise e

    async def verify(self):
        if not self.token:
            raise Unauthorized

        try:
            payload = await self.decode()
            exp_time = datetime.fromtimestamp(payload.get('exp'))

            if exp_time > datetime.now():
                return self.token

        except JWTError:
            raise Unauthorized

    async def create(self):
        user_data = await read_query('SELECT email,role FROM users WHERE user_id = %s', (self.user_id,))

        data_to_encode = {'user_id': self.user_id,
                          'email': user_data[0][0],
                          'role': user_data[0][1],
                          'exp': self.expiration}

        return await self.encode(data_to_encode)
