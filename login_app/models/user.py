import bcrypt

from login_app.database import read_query, update_query
from login_app.utils.responses import NotFound, EmailExists


class User:

    def __init__(self,email,password):
        self.email = email
        self.password = password

    async def authenticate(self):
        user_info = await read_query('SELECT * FROM users WHERE email = %s', (self.email,))

        if not user_info:
            raise NotFound

        if bcrypt.checkpw(self.password.encode('utf-8'), user_info[0][2].encode('utf-8')):
            return user_info[0][0]
        else:
            raise NotFound

    async def register(self):
        info = await read_query('SELECT * FROM users WHERE email = %s', (self.email,))
        if info:
            raise EmailExists

        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        await update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (self.email, hashed_password))
        return {"message": "User registered successfully!"}

