from login_app.models.access_token import AccessToken
from login_app.models.refresh_token import RefreshToken


class TokenService:

    def __init__(self, token):
        self.token = token

    async def verify_access_token(self):
        return await AccessToken(token=self.token, user_id=None).verify()

    async def verify_refresh_token(self):
        return await RefreshToken(token=self.token, user_id=None).verify()

    async def refresh_access_token(self):
        refresh_token_status = await RefreshToken(token=self.token, user_id=None).verify()
        access_token = await AccessToken(token=None, user_id=refresh_token_status['user_id']).create()

        return {'token': access_token, 'Validity': refresh_token_status['Validity']}

    async def refresh_refresh_token(self):
        refresh_token_status = await RefreshToken(token=self.token, user_id=None).verify()
        return await RefreshToken(token=None, user_id=refresh_token_status['user_id']).create()
