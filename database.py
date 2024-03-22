from typing import List, Dict
from pydantic import BaseModel
import json
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import asyncio
import dotenv
import os
dotenv.load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
database = client.coin
collection = database.get_collection("data")
class Token(BaseModel):
    address: str
    name: str
    symbol: str

class Txns(BaseModel):
    m5: Dict[str, int]
    h1: Dict[str, int]
    h6: Dict[str, int]
    h24: Dict[str, int]

class Volume(BaseModel):
    h24: float
    h6: float
    h1: float
    m5: float

class PriceChange(BaseModel):
    m5: float
    h1: float
    h6: float
    h24: float

class Liquidity(BaseModel):
    usd: float
    base: float
    quote: float

class Info(BaseModel):
    imageUrl: str
    websites: List[Dict[str, str]]
    socials: List[Dict[str, str]]

class Pair(BaseModel):
    chainId: str
    dexId: str
    url: str
    pairAddress: str
    baseToken: Token
    quoteToken: Token
    priceNative: str
    priceUsd: str
    txns: Txns
    volume: Volume
    priceChange: PriceChange
    liquidity: Liquidity
    pairCreatedAt: int
    info: Info

class Pairs(BaseModel):
    pairs: List[Pair]


## For initial entry of data in db
async def write_to_db():
    with open("data.json") as file:
        data = json.load(file)
        for token in data['pairs']:
            pair = Pair(**token)
            price = pair.priceUsd
            volume = pair.volume
            await collection.insert_one({
                "token": token['baseToken']['symbol'],
                'price': price,
                'volume': volume.model_dump(),
                
            })
    

