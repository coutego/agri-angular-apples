#!/usr/bin/env python3

import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import csv
import io
import os

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

# File path for CSV storage
CSV_FILE_PATH = "data/apple_stats.csv"

# Load records from CSV file
def load_records_from_csv():
    if not os.path.exists(CSV_FILE_PATH):
        return {}
    with open(CSV_FILE_PATH, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return {row["marketing_year"]: row for row in reader}

# Save records to CSV file
def save_records_to_csv(records: Dict[str, dict]):
    os.makedirs(os.path.dirname(CSV_FILE_PATH), exist_ok=True)
    with open(CSV_FILE_PATH, mode='w', newline='') as csvfile:
        fieldnames = [
            "marketing_year", "area", "yield", "total_production", "losses_and_feed",
            "usable_production", "fresh.production", "fresh.exports", "fresh.imports",
            "fresh.consumption", "fresh.per_capita_production", "fresh.ending_stocks",
            "fresh.stock_change", "fresh.self_sufficiency_rate", "processed.production",
            "processed.exports", "processed.imports", "processed.consumption",
            "processed.per_capita_production", "processed.self_sufficiency_rate",
            "per_capita_production"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records.values():
            # Flatten the nested dictionaries for CSV writing
            flat_record = {
                "marketing_year": record["marketing_year"],
                "area": record["area"],
                "yield": record["yield"],
                "total_production": record["total_production"],
                "losses_and_feed": record["losses_and_feed"],
                "usable_production": record["usable_production"],
                "fresh.production": record["fresh"]["production"],
                "fresh.exports": record["fresh"]["exports"],
                "fresh.imports": record["fresh"]["imports"],
                "fresh.consumption": record["fresh"]["consumption"],
                "fresh.per_capita_production": record["fresh"]["per_capita_production"],
                "fresh.ending_stocks": record["fresh"]["ending_stocks"],
                "fresh.stock_change": record["fresh"]["stock_change"],
                "fresh.self_sufficiency_rate": record["fresh"]["self_sufficiency_rate"],
                "processed.production": record["processed"]["production"],
                "processed.exports": record["processed"]["exports"],
                "processed.imports": record["processed"]["imports"],
                "processed.consumption": record["processed"]["consumption"],
                "processed.per_capita_production": record["processed"]["per_capita_production"],
                "processed.self_sufficiency_rate": record["processed"]["self_sufficiency_rate"],
                "per_capita_production": record["per_capita_production"]
            }
            writer.writerow(flat_record)

# In-memory database initialized from CSV
db: Dict[str, dict] = load_records_from_csv()

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
    
    save_records_to_csv(db)
    logging.info("File uploaded and saved successfully")
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
    save_records_to_csv(db)
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
    save_records_to_csv(db)
    logging.info("Bulk update of records and saved to CSV")
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
