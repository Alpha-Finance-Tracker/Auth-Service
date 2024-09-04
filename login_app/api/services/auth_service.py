from login_app.models.access_token import AccessToken
from login_app.models.refresh_token import RefreshToken
from login_app.models.user import User


class AuthService:

    def __init__(self,email,password):
        self.email = email
        self.password = password

    async def login(self):
        return await User(self.email,self.password).login()

    async def register(self):
        return await User(self.email,self.password).register()

