from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from auth.DatabaseController import connectToDB, closeDbConnection
from auth.routers import UserRoutes
from config import Config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connectToDB)
app.add_event_handler("shutdown", closeDbConnection)

@app.get("/")
async def root():
    return {"message": "Welcome to the api"}

app.include_router(UserRoutes.guest_router)
app.include_router(UserRoutes.auth_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)
