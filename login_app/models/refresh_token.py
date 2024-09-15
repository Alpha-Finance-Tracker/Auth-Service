import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt, JWTError

from login_app.models.base_models.token import Token
from login_app.utils.responses import Unauthorized

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


class RefreshToken(Token):
    REFRESH_TOKEN_EXPIRATION = 30  # Days

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

            time_remaining = exp_time - datetime.now()

            if time_remaining.total_seconds() > 172800:  # 2 days in seconds
                return {'Validity': 'Valid', 'token': self.token, 'user_id': payload.get('user_id')}
            else:
                return {'Validity': 'Expires', 'token': self.token, 'user_id': payload.get('user_id')}
        except JWTError:
            raise Unauthorized

    def create(self):
        expiration = datetime.now() + timedelta(days=self.REFRESH_TOKEN_EXPIRATION)

        data_to_encode = {'user_id': self.user.user_id,
                          'exp': expiration}
        return self.encode(data_to_encode)
