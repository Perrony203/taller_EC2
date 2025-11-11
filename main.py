from boto3.s3.transfer import S3Transfer
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI
from uuid import uuid4
import boto3
import json
import csv
import os
import io 

load_dotenv()

app = FastAPI()

s3 = boto3.client('s3')
transfer = S3Transfer(s3)

class Item(BaseModel):     
    nombre: str = Field(..., min_length=2, max_length=30)    
    edad: int = Field(..., ge=16, le=85)
    altura: int = Field(..., ge=100, le=220) 

@app.get("/items/", response_model=list[ItemResponse])
def read_items():
    obj = s3.get_object(Bucket=os.getenv("S3_BUCKET"), Key="persona.csv")
    csv_content = obj["Body"].read().decode("utf-8")

    # Contar líneas
    line_count = len(csv_content.strip().split("\n"))

    return {"Mensaje": "Número de líneas", "Data": line_count}
    
@app.post("/persona/")
def insert(item: Item):
    
    new_item = json.dumps({
        "id": uuid4(),
        "nombre": item.nombre,
        "edad": item.edad,
        "altura": item.altura,
        "createdAt": datetime.now()
    }, default = str)

    csv_buffer = io.StringIO()
    fieldnames = data[0].keys()

    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    
    s3.put_object(
    Bucket = os.getenv("S3_BUCKET"),
    Key = "persona.csv",
    Body=csv_buffer.getvalue(),
    ContentType="text/csv"
    )
    
    return {"Mensaje": "Item creado con éxito", "Data": new_item}