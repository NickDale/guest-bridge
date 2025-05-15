from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import users, authentication

app = FastAPI(root_path='/api')

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(authentication.router)
