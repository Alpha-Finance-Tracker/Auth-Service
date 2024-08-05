import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from login_app.api.auth_router import auth_router

app = FastAPI()
app.include_router(auth_router,tags=['Authentication'])


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
