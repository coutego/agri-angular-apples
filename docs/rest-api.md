# EU Apple Statistics REST API - PoC Version

## Base URL
`/api/v1/apples`

## Endpoints

### File Upload
```
POST /upload
Content-Type: multipart/form-data
```
Upload CSV file containing apple statistics data.

**Request Body:**
- `file`: CSV file (required)

**Response:**
- `201 Created` on success
- `400 Bad Request` if file format is invalid

### Get All Records
```
GET /records
```
Retrieve all apple statistics records.

**Response:**
```json
[
  {
    "marketing_year": "2021/2022",
    "area": 523.4,
    "yield": 35.2,
    "total_production": 18423.7,
    "losses_and_feed": 921.2,
    "usable_production": 17502.5,
    "fresh": {
      "production": 12251.7,
      "exports": 3245.6,
      "imports": 1523.4,
      "consumption": 10529.5,
      "per_capita_production": 27.5,
      "ending_stocks": 1523.4,
      "stock_change": 234.5,
      "self_sufficiency_rate": 116.4
    },
    "processed": {
      "production": 5250.8,
      "exports": 1234.5,
      "imports": 567.8,
      "consumption": 4584.1,
      "per_capita_production": 11.8,
      "self_sufficiency_rate": 114.5
    },
    "per_capita_production": 39.3
  }
]
```

### Get Single Record
```
GET /records/{marketing_year}
```
Retrieve a specific record by marketing year.

**Response:**
- `200 OK` with record data
- `404 Not Found` if record doesn't exist

### Update Record
```
PUT /records/{marketing_year}
Content-Type: application/json
```
Update an existing record.

**Request Body:** Single record JSON object

**Response:**
- `200 OK` on success
- `404 Not Found` if record doesn't exist

### Bulk Update
```
PUT /records
Content-Type: application/json
```
Update multiple records in a single request.

**Request Body:**
```json
[
  {
    "marketing_year": "2021/2022",
    // ... record fields
  },
  {
    "marketing_year": "2020/2021",
    // ... record fields
  }
]
```

**Response:**
- `200 OK` on success
- `400 Bad Request` if validation fails

## Error Response Format
```json
{
  "error": "Human readable error message"
}
```
