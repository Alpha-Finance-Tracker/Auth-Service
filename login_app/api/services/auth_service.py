# from login_app.models.user import User
import bcrypt

from login_app.database.models.user import User
from login_app.models.access_token import AccessToken
from login_app.models.refresh_token import RefreshToken
from login_app.utils.responses import NotFound, EmailExists


class AuthService:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    async def login(self):
        user_info = await self.authenticate()

        access_token = AccessToken(token=None, user=user_info).create()
        refresh_token = RefreshToken(token=None, user=user_info).create()

        return {
            "access_token": access_token,
            'refresh_token': refresh_token,
            "token_type": "bearer", }

    async def register(self):
        user_info = await User().get_user('email', self.email)
        if user_info:
            raise EmailExists()

        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        return await User().register(self.email, hashed_password)

    async def authenticate(self):
        user = await User().get_user('email', self.email)

        if not user:
            raise NotFound()

        if bcrypt.checkpw(self.password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            raise NotFound
