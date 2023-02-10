from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.books import router as BookRouter
from server.auth import router as AuthRouter
from server.AuthConfig.config import settings

app = FastAPI()

origins = []
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
app.include_router(BookRouter,tags=["Book"],prefix="/books")
app.include_router(AuthRouter,tags=['Auth'],prefix="/Auth")

@app.get("/",tags=['Root'])
async def read_root():
    return{"message":"Welcome!"}

