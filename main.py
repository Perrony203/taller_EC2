from boto3.s3.transfer import S3Transfer
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI
from uuid import uuid4
import boto3
import json
import os

load_dotenv()

app = FastAPI()

s3 = boto3.client('s3')
transfer = S3Transfer(s3)

class Item(BaseModel):     
    name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)
    edad: int = Field(..., ge=16, le=85)    

@app.post("/items/")
def insert(item: Item):
    
    new_item = json.dumps({
        "id": uuid4(),
        "name": item.name,
        "last_name": item.last_name,
        "edad": item.edad,
        "createdAt": datetime.now()
    }, default = str)

    cant = len(s3.list_objects_v2(Bucket=os.getenv("S3_BUCKET")).get('Contents', [])) + 1
    
    s3.put_object(
    Bucket = os.getenv("S3_BUCKET"),
    Key = f'persona-{cant}.json',
    Body = new_item,
    ContentType="application/json"
    )
    
    return {"Mensaje": "Item creado con éxito", "Data": new_item, "Cantidad de personas": cant}