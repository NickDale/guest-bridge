from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import users, authentication, accommodations

app = FastAPI(root_path='/api')

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(users.admin_router)
app.include_router(authentication.router)
app.include_router(accommodations.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
