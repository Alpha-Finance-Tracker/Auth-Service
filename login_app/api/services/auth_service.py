from login_app.models.access_token import AccessToken
from login_app.models.refresh_token import RefreshToken
from login_app.models.user import User


class AuthService:

    def __init__(self,email,password):
        self.email = email
        self.password = password

    async def login(self):
        user_id = await User(self.email,self.password).authenticate()

        access_token = await AccessToken(token=None,user_id=user_id).create()
        refresh_token = await RefreshToken(token=None,user_id=user_id).create()

        return {
            "access_token": access_token,
            'refresh_token': refresh_token,
            "token_type": "bearer",
        }

    async def register(self):
        return await User(self.email,self.password).register()

