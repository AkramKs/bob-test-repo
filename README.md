# Grocery Store API - FastAPI CRUD Backend

A CRUD FastAPI backend for managing grocery products in an online store.

## Features

- **Create** a new grocery product
- **Read** a single product by ID
- **Read** all products with optional filtering (by category, availability)
- **Update** product details (partial updates supported)
- **Delete** a product

## Product Schema

Each product has the following fields:
- `name` (required) - Product name
- `description` (optional) - Product description
- `price` (required) - Price (> 0)
- `category` (optional, default: "Other") - Product category
- `unit` (optional, default: "piece") - Unit of measurement (kg, liter, piece, etc.)
- `stock_quantity` (optional, default: 0) - Available stock quantity
- `is_available` (optional, default: true) - Whether the product is available

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message and docs link |
| POST | `/products/` | Create a new product |
| GET | `/products/` | List all products (with filters) |
| GET | `/products/{id}` | Get a product by ID |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload
```

3. Access the API documentation at `http://localhost:8000/docs`

## Running Tests

```bash
pytest -v
```
