from dotenv import dotenv_values

env_vars = dotenv_values()
HOST = env_vars.get("HOST")
USER = env_vars.get("USER")
PASSWORD = env_vars.get("PASSWORD")
PORT = env_vars.get("PORT")
DATABASE = env_vars.get("DATABASE")

DATABASE_URL = None

if all([HOST, USER, PASSWORD, PORT, DATABASE]):
    DATABASE_URL = f"mysql+asyncmy://{env_vars['USER']}:{env_vars['PASSWORD']}@{env_vars['HOST']}:{env_vars['PORT']}/{env_vars['DATABASE']}"
