from login_app.models.access_token import AccessToken
from login_app.models.refresh_token import RefreshToken
from login_app.database.models.user import User


class TokenService:

    def __init__(self, token):
        self.token = token

    async def verify_access_token(self):
        return await AccessToken(token=self.token, user=None).verify()

    async def verify_refresh_token(self):
        return await RefreshToken(token=self.token, user=None).verify()

    async def refresh_access_token(self):
        refresh_token_status = await RefreshToken(token=self.token, user=None).verify()
        user = await User().get_user('user_id', refresh_token_status['user_id'])

        access_token = await AccessToken(token=None, user=user).create()
        return {'token': access_token, 'Validity': refresh_token_status['Validity']}

    async def refresh_refresh_token(self):
        refresh_token_status = await RefreshToken(token=self.token, user=None).verify()

        user = await User().get_user('user_id', refresh_token_status['user_id'])
        return await RefreshToken(token=None, user=user).create()
