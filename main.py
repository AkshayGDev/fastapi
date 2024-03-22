from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import dotenv
import os
import uvicorn
import json
from database import Pair as Data
from bson import json_util
from bson import ObjectId

dotenv.load_dotenv()

app = FastAPI()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
database = client.coin
collection = database.get_collection("data")


##Data filters
def filter_data(data):
    return {"price": data.priceUsd, "volume": data.volume}


@app.get("/data")
async def get_data():
    data = []
    async for document in collection.find():
        document["_id"] = str(document["_id"])
        data.append(document)
    return {"data": data}


@app.post("/data")
async def create_data(data: Data):

    result = await collection.insert_one(filter_data(data))
    return {"id": str(result.inserted_id)}


@app.get("/data/{data_id}")
async def read_data(data_id: str):
    try:
        data = await collection.find_one({"_id": ObjectId(data_id)})
        if data:
            data["_id"] = str(data["_id"])
            return data
        raise HTTPException(status_code=404, detail="Data not found")
    except:
        raise HTTPException(status_code=400, detail="Id Invalid Format")


@app.put("/data/{data_id}")
async def update_data(data_id: str, data: Data):
    result = await collection.update_one(
        {"_id": ObjectId(data_id)}, {"$set": filter_data(data.model_dump())}
    )

    if result.modified_count == 1:
        if data:
            data["_id"] = str(data["_id"])
            return data
    raise HTTPException(status_code=404, detail="Data not found")


@app.delete("/data/{data_id}")
async def delete_data(data_id: str):
    result = await collection.delete_one({"_id": ObjectId(data_id)})
    if result.deleted_count == 1:
        return {"message": "Data deleted successfully"}
    raise HTTPException(status_code=404, detail="Data not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
