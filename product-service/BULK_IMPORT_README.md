# Bulk Product Import API

This API allows you to bulk import products from a CSV file with comprehensive validation and error handling.

## Endpoints

### 1. Download Template
```
GET /products/bulk-import/template
```
Downloads a CSV template with the correct headers and sample data.

### 2. Bulk Import
```
POST /products/bulk-import
```
Upload a CSV file to bulk create products.

## CSV Format

### Required Headers
- `name`: Product name (string)
- `short_name`: Product short name (string)
- `category`: Level2 category ID (ObjectId string)
- `price`: Product price (float)
- `description`: Product description (string)
- `currency_code`: Currency code (string, e.g., "USD", "EUR")
- `width`: Width in mm (float)
- `length`: Length in mm (float)
- `height`: Height in mm (float)
- `depth`: Depth in mm (float, optional)
- `weight`: Weight in grams (float, optional)
- `colors`: Comma-separated color codes (string)
- `material_id`: Material ID (ObjectId string)

### Sample CSV
```csv
name,short_name,category,price,description,currency_code,width,length,height,depth,weight,colors,material_id
"Oak Dining Table","Oak Table","507f1f77bcf86cd799439011",299.99,"Beautiful oak dining table for 6 people","USD",1200,800,750,50,25000,"oak_brown,walnut_brown","507f1f77bcf86cd799439012"
"Leather Sofa","Leather Sofa","507f1f77bcf86cd799439013",599.99,"Comfortable leather sofa with premium finish","USD",2000,800,850,90,45000,"brown,black","507f1f77bcf86cd799439014"
```

## Validation Rules

### File Validation
- File must be CSV format
- Maximum file size: 10MB
- All required headers must be present

### Data Validation
- Required fields cannot be empty
- Numeric fields must be valid numbers
- ObjectIds must be valid MongoDB ObjectId format
- Category and Material IDs must exist in the database
- Colors should be comma-separated

### Error Handling
- Individual row validation errors are collected
- Valid products are imported even if some rows fail
- Detailed error messages for each failed row
- Returns count of successful imports

## Features

### Decorators
1. **@validate_csv_file**: Validates file format and size
2. **@validate_csv_headers**: Validates required CSV headers
3. **@log_bulk_operation**: Logs operation timing and results

### Logging
- Start and end timestamps
- Operation duration
- Success/failure status
- Number of products imported
- Detailed error logging

### Bulk Operations
- Uses MongoDB's `insert_many()` for efficient bulk insertion
- Transaction-like behavior with rollback on errors
- Returns inserted ObjectIds for successful imports

## Response Format

### Success Response
```json
{
  "class_name": "BulkProductImport",
  "status_code": 201,
  "message": "Successfully imported 5 products",
  "data": {
    "imported_count": 5,
    "inserted_ids": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"]
  }
}
```

### Error Response
```json
{
  "detail": {
    "message": "Validation errors found",
    "errors": [
      "Row 3: Missing required fields",
      "Row 5: Invalid numeric values"
    ],
    "valid_products_count": 3
  }
}
```

## Usage Examples

### Using curl
```bash
# Download template
curl -X GET "http://localhost:8000/products/bulk-import/template" \
  -o template.csv

# Upload CSV file
curl -X POST "http://localhost:8000/products/bulk-import" \
  -F "file=@products.csv"
```

### Using Python requests
```python
import requests

# Download template
response = requests.get("http://localhost:8000/products/bulk-import/template")
with open("template.csv", "wb") as f:
    f.write(response.content)

# Upload CSV file
with open("products.csv", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/products/bulk-import", files=files)
    print(response.json())
```

## Performance Considerations

- File size limit: 10MB
- Recommended batch size: 1000 products per file
- Processing time: ~1 second per 100 products
- Memory usage: Scales with file size

## Error Recovery

- Partial imports are supported
- Valid products are imported even if some rows fail
- Detailed error reporting for failed rows
- No database corruption on validation errors

## Security Features

- File type validation
- File size limits
- Input sanitization
- SQL injection prevention (MongoDB)
- Comprehensive error handling 