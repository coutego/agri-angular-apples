#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import csv
import io

app = FastAPI(title="EU Apple Statistics API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
db: Dict[str, dict] = {}

@app.post("/api/v1/apples/upload", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    csv_data = csv.DictReader(io.StringIO(content.decode()))
    
    for row in csv_data:
        marketing_year = row["marketing_year"]
        db[marketing_year] = row
    
    return {"message": "File uploaded successfully"}

@app.get("/api/v1/apples/records")
async def get_all_records():
    return list(db.values())

@app.get("/api/v1/apples/records/{marketing_year}")
async def get_record(marketing_year: str):
    if marketing_year not in db:
        raise HTTPException(status_code=404, detail="Record not found")
    return db[marketing_year]

@app.put("/api/v1/apples/records/{marketing_year}")
async def update_record(marketing_year: str, record: dict):
    if marketing_year not in db:
        raise HTTPException(status_code=404, detail="Record not found")
    db[marketing_year] = record
    return db[marketing_year]

@app.put("/api/v1/apples/records")
async def bulk_update(records: List[dict]):
    for record in records:
        marketing_year = record.get("marketing_year")
        if not marketing_year:
            raise HTTPException(status_code=400, detail="Marketing year is required")
        db[marketing_year] = record
    return {"message": "Records updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
