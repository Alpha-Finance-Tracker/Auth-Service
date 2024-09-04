from login_app.models.user import User


class AuthService:

    def __init__(self,email,password):
        self.email = email
        self.password = password

    async def login(self):
        return await User(self.email,self.password).login()

    async def register(self):
        return await User(self.email,self.password).register()
