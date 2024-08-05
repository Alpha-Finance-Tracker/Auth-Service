import bcrypt

from login_app.data.database import read_query, update_query


def check_if_email_is_already_registered(email):
    return True if read_query('SELECT email FROM users WHERE email = %s', (email,)) != [] else False

def authenticate_user_service(email):
    return read_query('SELECT email, password FROM users WHERE email = %s', (email,))


def login_service(email):
    return read_query('SELECT * FROM users WHERE email = %s', (email,))

def register_service(email,password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    update_query('INSERT INTO users(email,password) VALUES(%s, %s)', (email, hashed_password))
    return {"message": "User registered successfully!"}