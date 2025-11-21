# Quick Start Guide - Creating a New Model (Products Example)

This guide walks you through the complete process of setting up the project and creating a new model with CRUD operations, using a Products model as an example.

---

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [Creating the Products Model](#creating-the-products-model)
3. [Testing the API](#testing-the-api)
4. [Verification](#verification)

---

## Initial Setup

### Step 0: Clone the Repository

First, clone the repository to your local machine:

**Using HTTPS:**
```bash
git clone https://github.com/dinnovos/agent-base-project.git
cd agent-base-project
```

**Using SSH:**
```bash
git clone git@github.com:dinnovos/agent-base-project.git
cd agent-base-project
```

**Using GitHub CLI:**
```bash
gh repo clone dinnovos/agent-base-project
cd agent-base-project
```

> **Tip:** If you want to create your own project based on this template, click the "Use this template" button on GitHub instead of cloning.

### Step 1: Install uv

First, install `uv` if you haven't already:

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment and install dependencies in one command
uv sync
```

This will:
- Create a `.venv` virtual environment automatically
- Install all dependencies from `pyproject.toml`
- Be much faster than traditional pip

**Alternative:** If you prefer using `requirements.txt`:
```bash
# Create virtual environment
uv venv

# Activate it (Windows PowerShell)
.venv\Scripts\activate

# Activate it (Windows CMD)
.venv\Scripts\activate.bat

# Activate it (Linux/Mac)
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

You should see `(.venv)` at the beginning of your terminal prompt.

### Step 3: Verify Installation

All required packages are now installed, including:
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- Pydantic
- LangGraph and LangChain
- And more...

### Step 4: Configure Environment Variables

**Windows:**
```bash
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Generate a secure SECRET_KEY:**
```bash
# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and replace `your-super-secret-key-here-change-in-production` in your `.env` file.

### Step 5: Initialize Database

Create the initial database migration:
```bash
alembic revision --autogenerate -m "initial migration"
```

Apply the migration to create tables:
```bash
alembic upgrade head
```

### Step 6: Run the Application

#### Windows (Development)

**⚠️ Important**: Due to psycopg async driver requirements on Windows, use one of these methods:

**Option 1 - Using run.py (Recommended):**
```bash
python run.py
```

**Option 2 - Using uvicorn with loop parameter:**
```bash
uvicorn src.main:app --reload --loop asyncio
```

#### Linux/macOS (Development)

```bash
# Using run.py
python run.py

# Or using uvicorn directly
uvicorn src.main:app --reload
```

#### Production (Railway/Docker)

No special configuration needed - works out of the box:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

> **Note**: The Windows-specific configuration is only needed for local development. Railway and Docker use Linux containers and work without any special setup.

---

## Creating the Products Model

Now let's create a complete CRUD implementation for a Products model with the following fields:
- `id` (Integer, Primary Key)
- `title` (String)
- `description` (Text)
- `status` (String)

### Step 1: Create the Database Model

Create a new file `src/models/product.py`:

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.models.base import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active", nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**Key Points:**
- Inherits from `Base` (SQLAlchemy declarative base)
- `__tablename__` defines the database table name
- `id` is the primary key with auto-increment
- `title` is indexed for faster queries
- `status` has a default value of "active"
- Timestamps are automatically managed

### Step 2: Create Pydantic Schemas

Create a new file `src/schemas/product.py`:

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema with common fields."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: str = Field(default="active", max_length=50)


class ProductCreate(ProductBase):
    """Schema for product creation."""
    pass


class ProductUpdate(BaseModel):
    """Schema for product update (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=50)


class ProductRead(ProductBase):
    """Schema for product output."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**Schema Breakdown:**
- **ProductBase**: Common fields shared between create and read operations
- **ProductCreate**: Used when creating a new product (inherits from ProductBase)
- **ProductUpdate**: All fields optional for partial updates
- **ProductRead**: Includes database-generated fields (id, timestamps)

### Step 3: Create Service Layer

Create a new file `src/services/product_service.py`:

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.product import Product
from src.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Get a single product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Get all products with pagination."""
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product_data: ProductCreate) -> Product:
    """Create a new product."""
    db_product = Product(
        title=product_data.title,
        description=product_data.description,
        status=product_data.status
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
    """Update an existing product."""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete a product."""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return True
```

**Service Functions:**
- **get_product**: Retrieve a single product by ID
- **get_products**: List all products with pagination
- **create_product**: Create a new product
- **update_product**: Update existing product (partial updates supported)
- **delete_product**: Delete a product

### Step 4: Create API Router

Create a new file `src/routers/products.py`:

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.user import User
from src.schemas.product import ProductCreate, ProductRead, ProductUpdate
from src.services.product_service import (
    get_product,
    get_products,
    create_product,
    update_product,
    delete_product
)
from src.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all products with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    products = get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific product by ID.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new product.
    
    - **title**: Product title (required)
    - **description**: Product description (optional)
    - **status**: Product status (default: "active")
    """
    product = create_product(db, product_data)
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def update_existing_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing product (partial update).
    
    All fields are optional - only provided fields will be updated.
    """
    product = update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a product.
    """
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return None
```

**Endpoint Overview:**
- **GET /products/**: List all products (with pagination)
- **GET /products/{id}**: Get a specific product
- **POST /products/**: Create a new product
- **PATCH /products/{id}**: Update a product
- **DELETE /products/{id}**: Delete a product

All endpoints require authentication (JWT token).

### Step 5: Register Router in Main Application

Edit `src/main.py` to include the products router.

Find the section where routers are imported and add:
```python
from src.routers import auth, users, profiles, products
```

Then find where routers are included and add:
```python
app.include_router(products.router)
```

The complete section should look like:
```python
# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(products.router)
```

### Step 6: Create Database Migration

Generate a new migration for the products table:
```bash
alembic revision --autogenerate -m "add products table"
```

Apply the migration:
```bash
alembic upgrade head
```

This creates the `products` table in your database.

### Step 7: Restart the Application

Stop the running server (Ctrl+C) and restart it:
```bash
python run.py
```

---

## Testing the API

### Create Test File

Create a new file `api_products.http` in the project root:

```http
### Variables
@baseUrl = http://localhost:8000
@token = YOUR_TOKEN_HERE

### ============================================
### Authentication (Get Token First)
### ============================================

### Register New User
POST {{baseUrl}}/auth/register HTTP/1.1
Content-Type: application/json

{
  "email": "testuser@example.com",
  "username": "testuser",
  "password": "SecurePassword123",
  "first_name": "Test",
  "last_name": "User"
}

### Login to Get Token
POST {{baseUrl}}/auth/login HTTP/1.1
Content-Type: application/json

{
  "email": "testuser@example.com",
  "password": "SecurePassword123"
}

# Copy the access_token from the response above and paste it in the @token variable

### ============================================
### Products CRUD Operations
### ============================================

### Create Product #1
POST {{baseUrl}}/products/ HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Laptop Dell XPS 15",
  "description": "High-performance laptop with 16GB RAM and 512GB SSD",
  "status": "active"
}

### Create Product #2
POST {{baseUrl}}/products/ HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "status": "active"
}

### Create Product #3 (Minimal - only required fields)
POST {{baseUrl}}/products/ HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "USB-C Cable"
}

### Get All Products
GET {{baseUrl}}/products/ HTTP/1.1
Authorization: Bearer {{token}}

### Get All Products with Pagination
GET {{baseUrl}}/products/?skip=0&limit=10 HTTP/1.1
Authorization: Bearer {{token}}

### Get Product by ID (replace 1 with actual product ID)
GET {{baseUrl}}/products/1 HTTP/1.1
Authorization: Bearer {{token}}

### Update Product (Partial Update)
PATCH {{baseUrl}}/products/1 HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": "Laptop Dell XPS 15 - Updated",
  "status": "inactive"
}

### Update Product (Single Field)
PATCH {{baseUrl}}/products/2 HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "description": "Updated description for wireless mouse"
}

### Delete Product
DELETE {{baseUrl}}/products/3 HTTP/1.1
Authorization: Bearer {{token}}

### ============================================
### Error Cases (for testing)
### ============================================

### Get Non-Existent Product (Should return 404)
GET {{baseUrl}}/products/9999 HTTP/1.1
Authorization: Bearer {{token}}

### Create Product without Authentication (Should return 401)
POST {{baseUrl}}/products/ HTTP/1.1
Content-Type: application/json

{
  "title": "Unauthorized Product"
}

### Create Product with Invalid Data (Should return 422)
POST {{baseUrl}}/products/ HTTP/1.1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "title": ""
}
```

### Testing Steps

1. **Get Authentication Token:**
   - Execute the "Register New User" request (or skip if user exists)
   - Execute the "Login to Get Token" request
   - Copy the `access_token` from the response
   - Replace `YOUR_TOKEN_HERE` in the `@token` variable at the top

2. **Create Products:**
   - Execute "Create Product #1" - Should return 201 Created
   - Execute "Create Product #2" - Should return 201 Created
   - Execute "Create Product #3" - Should return 201 Created

3. **Read Products:**
   - Execute "Get All Products" - Should return array of all products
   - Execute "Get Product by ID" - Should return single product

4. **Update Products:**
   - Execute "Update Product (Partial Update)" - Should return updated product
   - Execute "Update Product (Single Field)" - Should update only description

5. **Delete Product:**
   - Execute "Delete Product" - Should return 204 No Content

6. **Test Error Cases:**
   - Execute error case requests to verify proper error handling

---

## Verification

### Check API Documentation

Visit http://localhost:8000/docs to see the interactive Swagger documentation.

You should see a new "Products" section with all CRUD endpoints.

### Verify Database

Check that the products table was created:

**SQLite:**
```bash
sqlite3 app.db
.tables
SELECT * FROM products;
.quit
```

**PostgreSQL:**
```bash
psql -d your_database
\dt
SELECT * FROM products;
\q
```

### Run Tests (Optional)

Create a test file `tests/test_products.py`:

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_product_unauthorized():
    """Test creating product without authentication."""
    response = client.post(
        "/products/",
        json={"title": "Test Product"}
    )
    assert response.status_code == 401


def test_product_crud_flow(auth_headers):
    """Test complete CRUD flow for products."""
    # Create
    response = client.post(
        "/products/",
        json={
            "title": "Test Product",
            "description": "Test Description",
            "status": "active"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    product_id = response.json()["id"]
    
    # Read
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Product"
    
    # Update
    response = client.patch(
        f"/products/{product_id}",
        json={"title": "Updated Product"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Product"
    
    # Delete
    response = client.delete(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify deletion
    response = client.get(f"/products/{product_id}", headers=auth_headers)
    assert response.status_code == 404
```

Run tests:
```bash
pytest tests/test_products.py -v
```

---

## Summary

You've successfully:

✅ Set up the virtual environment  
✅ Installed all dependencies  
✅ Configured environment variables  
✅ Initialized the database with Alembic  
✅ Created a complete Products model with:
  - Database model (`src/models/product.py`)
  - Pydantic schemas (`src/schemas/product.py`)
  - Service layer (`src/services/product_service.py`)
  - API router (`src/routers/products.py`)  
✅ Registered the router in the main application  
✅ Created and applied database migrations  
✅ Created comprehensive API tests in `.http` file  
✅ Verified the implementation

---

## Next Steps

To create additional models, follow the same pattern:

1. Create model in `src/models/`
2. Create schemas in `src/schemas/`
3. Create service in `src/services/`
4. Create router in `src/routers/`
5. Register router in `src/main.py`
6. Generate and apply migration
7. Create tests in `api.http` or `tests/`

---

## Common Issues and Solutions

### Issue: "Module not found" errors
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
uv sync
```

Or if using requirements.txt:
```bash
uv pip install -r requirements.txt
```

### Issue: Database migration fails
**Solution:** Check that DATABASE_URL is correct in `.env` and database is accessible

### Issue: "Could not validate credentials" error
**Solution:** Ensure you're using a valid token and it hasn't expired (tokens expire after 30 minutes by default)

### Issue: 422 Validation Error
**Solution:** Check that all required fields are provided and data types match the schema

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **Pydantic Documentation**: https://docs.pydantic.dev/

---

**Happy Coding! 🚀**
