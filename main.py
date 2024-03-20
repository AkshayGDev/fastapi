from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import dotenv
import os
dotenv.load_dotenv()

app=FastAPI()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
database = client["sample_mflix"]
collection = database["comments"]

print(collection)
