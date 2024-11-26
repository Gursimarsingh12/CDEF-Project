from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi import HTTPException
from config import Config

client: Optional[AsyncIOMotorClient] = None

async def connectToDB():
    global client
    if client is None:
        try:
            mongo_uri = Config.MONGO_URI
            client = AsyncIOMotorClient(mongo_uri)
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise HTTPException(status_code=500, detail="Database connection error")

async def closeDbConnection():
    global client
    if client is not None:
        client.close()
        print("MongoDB connection closed")

async def getUsersCollection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.cdef
    return db.get_collection("users")

async def getTokenCollection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.cdef
    return db.get_collection("tokens")

async def getTranscriptionCollection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.cdef
    return db.get_collection("transcriptions")

async def getSummarizationCollection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.cdef
    return db.get_collection("summarizations")