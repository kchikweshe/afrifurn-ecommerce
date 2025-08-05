# Product Lookup Aggregation with $lookup

This document describes the implementation of MongoDB aggregation pipelines using `$lookup` to populate referenced collections and add them to product objects.

## Overview

The lookup aggregation system provides a powerful way to fetch products with all their referenced data in a single query, eliminating the need for multiple database calls and improving performance.

## Features

### 🔗 **Complete Relationship Population**
- **Category Hierarchy**: Category → Level1Category → Level2Category
- **Currency**: Full currency details with code and symbol
- **Colors**: Complete color information including images
- **Variants**: Product variants with stock quantities
- **Reviews**: Product reviews with ratings and user info

### 📊 **Computed Fields**
- `total_reviews`: Count of reviews per product
- `average_rating`: Average rating across all reviews
- `total_stock`: Sum of all variant stock quantities
- `available_colors`: Formatted color information

## Implementation

### ProductPipeline.get_products_with_lookups()

The main method that generates the aggregation pipeline:

```python
@staticmethod
def get_products_with_lookups(
    query_criteria: Optional[dict] = None,
    sort_by: str = "_id",
    sort_order: int = 1,
    skip: int = 0,
    limit: int = 10
) -> List[Dict[str, Any]]:
```

**Parameters:**
- `query_criteria`: MongoDB match criteria for filtering products
- `sort_by`: Field to sort by
- `sort_order`: Sort order (1 for ascending, -1 for descending)
- `skip`: Number of documents to skip (for pagination)
- `limit`: Maximum number of documents to return

**Returns:**
- Complete MongoDB aggregation pipeline

## Pipeline Structure

The lookup pipeline consists of the following stages:

### 1. **$match** - Filter Products
```javascript
{"$match": query_criteria}
```

### 2. **$lookup** Stages - Populate References

#### Category Hierarchy Lookups
```javascript
// Level2Category lookup
{
  "$lookup": {
    "from": "level2_categories",
    "localField": "category",
    "foreignField": "_id",
    "as": "category_data"
  }
}

// Level1Category lookup
{
  "$lookup": {
    "from": "level1_categories", 
    "localField": "category_data.level_one_category",
    "foreignField": "_id",
    "as": "level1_category_data"
  }
}

// Category lookup
{
  "$lookup": {
    "from": "categories",
    "localField": "level1_category_data.category",
    "foreignField": "_id",
    "as": "main_category_data"
  }
}
```

#### Currency Lookup
```javascript
{
  "$lookup": {
    "from": "currencies",
    "localField": "currency",
    "foreignField": "_id",
    "as": "currency_data"
  }
}
```

#### Colors Lookup
```javascript
{
  "$lookup": {
    "from": "colors",
    "localField": "color_codes",
    "foreignField": "_id",
    "as": "colors_data"
  }
}
```

#### Variants Lookup
```javascript
{
  "$lookup": {
    "from": "variants",
    "localField": "_id",
    "foreignField": "product_id",
    "as": "variants_data"
  }
}
```

#### Reviews Lookup
```javascript
{
  "$lookup": {
    "from": "reviews",
    "localField": "_id",
    "foreignField": "product_id",
    "as": "reviews_data"
  }
}
```

### 3. **$addFields** - Add Computed Fields
```javascript
{
  "$addFields": {
    "populated_category": {
      "$cond": {
        "if": {"$gt": [{"$size": "$category_data"}, 0]},
        "then": {"$arrayElemAt": ["$category_data", 0]},
        "else": null
      }
    },
    "total_reviews": {"$size": "$reviews_data"},
    "average_rating": {
      "$cond": {
        "if": {"$gt": [{"$size": "$reviews_data"}, 0]},
        "then": {"$avg": "$reviews_data.rating"},
        "else": 0
      }
    },
    "total_stock": {
      "$sum": "$variants_data.quantity_in_stock"
    }
  }
}
```

### 4. **$project** - Final Structure
```javascript
{
  "$project": {
    "_id": 1,
    "name": 1,
    "price": 1,
    // ... other product fields
    
    // Populated references
    "category": "$populated_category",
    "currency": "$populated_currency",
    "colors": "$populated_colors",
    "variants": "$populated_variants",
    "reviews": "$populated_reviews",
    
    // Computed fields
    "total_reviews": 1,
    "average_rating": 1,
    "total_stock": 1
  }
}
```

### 5. **Sort and Paginate**
```javascript
{"$sort": {sort_by: sort_order}},
{"$skip": skip},
{"$limit": limit}
```

## API Endpoint

### `/filter-with-lookups`

**Route:** `GET /products/filter-with-lookups`

**Query Parameters:**
- All standard filter parameters from the original `/filter` endpoint
- Returns products with all referenced collections populated

**Example Usage:**
```bash
GET /products/filter-with-lookups?page=1&page_size=10&sort_by=price&sort_order=1
```

**Response Structure:**
```json
{
  "_id": "product_id",
  "name": "Oak Dining Table",
  "description": "Beautiful oak dining table",
  "price": 599.99,
  "category": {
    "_id": "level2_category_id",
    "name": "Dining Tables",
    "description": "Dining table category"
  },
  "level1_category": {
    "_id": "level1_category_id",
    "name": "Tables",
    "description": "Table category"
  },
  "main_category": {
    "_id": "category_id",
    "name": "Furniture",
    "description": "Main furniture category"
  },
  "currency": {
    "_id": "currency_id",
    "code": "USD",
    "symbol": "$"
  },
  "colors": [
    {
      "_id": "color_id",
      "name": "Oak",
      "color_code": "#8B4513",
      "image": "oak.jpg"
    }
  ],
  "variants": [
    {
      "_id": "variant_id",
      "color_id": "color_id",
      "quantity_in_stock": 5,
      "images": ["table1.jpg", "table2.jpg"]
    }
  ],
  "reviews": [
    {
      "_id": "review_id",
      "user_id": "user_id",
      "rating": 5,
      "title": "Great table!",
      "description": "Excellent quality"
    }
  ],
  "total_reviews": 10,
  "average_rating": 4.5,
  "total_stock": 15,
  "available_colors": [
    {
      "id": "color_id",
      "name": "Oak",
      "color_code": "#8B4513",
      "image": "oak.jpg"
    }
  ]
}
```

## Usage Examples

### Basic Filtering
```python
from models.products import ProductPipeline

# Get all active products with lookups
pipeline = ProductPipeline.get_products_with_lookups(
    query_criteria={"is_archived": False},
    sort_by="created_at",
    sort_order=-1,
    skip=0,
    limit=10
)
```

### Price Range Filtering
```python
# Filter products between $100 and $500
query_criteria = {
    "is_archived": False,
    "price": {"$gte": 100, "$lte": 500}
}

pipeline = ProductPipeline.get_products_with_lookups(
    query_criteria=query_criteria,
    sort_by="price",
    sort_order=1
)
```

### Category Filtering
```python
# Filter by specific category
query_criteria = {
    "is_archived": False,
    "category": "level2_category_id"
}

pipeline = ProductPipeline.get_products_with_lookups(
    query_criteria=query_criteria,
    sort_by="name",
    sort_order=1
)
```

### Color Filtering
```python
# Filter products with specific colors
query_criteria = {
    "is_archived": False,
    "color_codes": {"$in": ["color_id_1", "color_id_2"]}
}

pipeline = ProductPipeline.get_products_with_lookups(
    query_criteria=query_criteria
)
```

### Complex Filtering
```python
# Multiple criteria
query_criteria = {
    "is_archived": False,
    "price": {"$gte": 200, "$lte": 1000},
    "material": {"$regex": "wood", "$options": "i"},
    "is_new": True
}

pipeline = ProductPipeline.get_products_with_lookups(
    query_criteria=query_criteria,
    sort_by="created_at",
    sort_order=-1
)
```

## Performance Considerations

### Indexes Required
Ensure the following indexes exist for optimal performance:

```javascript
// Products collection
db.products.createIndex({"category": 1})
db.products.createIndex({"currency": 1})
db.products.createIndex({"color_codes": 1})
db.products.createIndex({"is_archived": 1})
db.products.createIndex({"price": 1})
db.products.createIndex({"material": 1})

// Variants collection
db.variants.createIndex({"product_id": 1})

// Reviews collection
db.reviews.createIndex({"product_id": 1})

// Categories
db.level2_categories.createIndex({"_id": 1})
db.level1_categories.createIndex({"_id": 1})
db.categories.createIndex({"_id": 1})

// Colors
db.colors.createIndex({"_id": 1})

// Currencies
db.currencies.createIndex({"_id": 1})
```

### Memory Usage
- Large result sets may consume significant memory
- Consider implementing cursor-based pagination for large datasets
- Monitor aggregation memory usage in MongoDB

### Caching
- The endpoint uses Redis caching with 5-minute TTL
- Cache keys include all filter parameters
- Consider implementing cache warming for popular filters

## Testing

### Test Script
Run the test script to see the lookup pipeline in action:

```bash
python test_lookup_pipeline.py
```

### Examples
Run the examples to see different filtering scenarios:

```bash
python examples/lookup_examples.py
```

## Error Handling

The implementation handles the following error scenarios:

- **Invalid ObjectId**: Returns 400 Bad Request
- **Database Connection Issues**: Returns 500 Internal Server Error
- **Invalid Query Parameters**: Returns 400 Bad Request with detailed error message

## Monitoring and Debugging

### Logging
- All pipeline stages are logged for debugging
- Query criteria and result counts are logged
- Error details are logged with stack traces

### Performance Monitoring
Monitor the following metrics:
- Aggregation execution time
- Memory usage during aggregation
- Cache hit rates
- Database connection pool usage

### Debugging Queries
Use MongoDB's `explain()` to analyze query performance:

```javascript
db.products.aggregate(pipeline).explain("executionStats")
```

## Benefits

### 🚀 **Performance**
- Single database query instead of multiple queries
- Reduced network round trips
- Efficient data transfer

### 🎯 **Data Completeness**
- All referenced data available in one response
- No missing relationships
- Consistent data structure

### 🔧 **Flexibility**
- Easy to extend with additional lookups
- Configurable sorting and pagination
- Reusable pipeline builder

### 📊 **Computed Fields**
- Real-time calculations (reviews, ratings, stock)
- No need for separate aggregation queries
- Consistent computed values

## Future Enhancements

1. **Faceted Search**: Add aggregation for filter facets
2. **Full-Text Search**: Integrate with MongoDB Atlas Search
3. **Geospatial Queries**: Add location-based filtering
4. **Real-time Updates**: Implement change streams for live updates
5. **GraphQL Support**: Add GraphQL schema for flexible queries
6. **Caching Strategy**: Implement more sophisticated caching
7. **Performance Optimization**: Add query optimization hints 