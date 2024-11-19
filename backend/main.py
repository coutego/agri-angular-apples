#!/usr/bin/env python3

import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import csv
import io

def configure_logging(log_level: str):
    if log_level == 'none':
        logging.basicConfig(level=logging.CRITICAL)
    elif log_level == 'generic':
        logging.basicConfig(level=logging.INFO)
    elif log_level == 'detailed':
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

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
    logging.info("File upload initiated")
    csv_data = csv.DictReader(io.StringIO(content.decode()))
    
    for row in csv_data:
        marketing_year = row["marketing_year"]
        db[marketing_year] = row
    
    logging.info("File uploaded successfully")
    return {"message": "File uploaded successfully"}

@app.get("/api/v1/apples/records")
async def get_all_records():
    logging.info("Fetching all records")
    return list(db.values())

@app.get("/api/v1/apples/records/{marketing_year}")
async def get_record(marketing_year: str):
    if marketing_year not in db:
        raise HTTPException(status_code=404, detail="Record not found")
    logging.info(f"Fetching record for marketing year: {marketing_year}")
    logging.info(f"Updating record for marketing year: {marketing_year}")
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
    logging.info("Bulk update of records")
    return {"message": "Records updated successfully"}

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Run the EU Apple Statistics API")
    parser.add_argument('--log', choices=['none', 'generic', 'detailed'], default='generic', help='Set the logging level')
    args = parser.parse_args()

    configure_logging(args.log)
    logging.info("Starting the EU Apple Statistics API")
    uvicorn.run(app, host="127.0.0.1", port=8000)
