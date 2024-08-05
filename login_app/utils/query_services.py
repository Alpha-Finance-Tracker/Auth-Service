import bcrypt
from login_app.data.database import read_query, update_query
from login_app.utils.responses import NotFound, EmailExists


async def authenticate_user(email: str, password: str):
    user_info = read_query('SELECT * FROM users WHERE email = %s', (email,))

    if not user_info:
        raise NotFound


    if bcrypt.checkpw(password.encode('utf-8'), user_info[0][2].encode('utf-8')):
        return user_info
    else:
        raise NotFound


async def register_service(email, password):
    info = read_query('SELECT * FROM users WHERE email = %s', (email,))
    if info != []:
        raise EmailExists


    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (email, hashed_password))
    return {"message": "User registered successfully!"}
