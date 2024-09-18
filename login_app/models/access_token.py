import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt, JWTError
from login_app.models.base_models.token import Token
from login_app.utils.responses import Unauthorized

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


class AccessToken(Token):
    ACCESS_TOKEN_EXPIRATION = 15  # Min

    def __init__(self, token, user):
        self.token = token
        self.user = user

    def encode(self, data):
        try:
            return jwt.encode(data, secret_key, algorithm)
        except Exception as e:
            raise e

    def decode(self):
        try:
            return jwt.decode(self.token, secret_key, algorithms=[algorithm])
        except Exception as e:
            raise e

    def verify(self):
        if not self.token:
            raise Unauthorized

        try:
            payload = self.decode()
            exp_time = datetime.fromtimestamp(payload.get('exp'))

            if exp_time > datetime.now():
                return self.token

        except JWTError:
            raise Unauthorized

    def create(self):
        expiration = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRATION)

        data_to_encode = {'user_id': self.user.user_id,
                          'email': self.user.email,
                          'role': self.user.role,
                          'exp': expiration}

        return self.encode(data_to_encode)
