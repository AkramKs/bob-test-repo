from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    description: Optional[str] = Field(default="", max_length=500, description="Description of the product")
    price: float = Field(..., gt=0, description="Price of the product")
    category: Optional[str] = Field(default="Other", max_length=50, description="Category of the product")
    unit: Optional[str] = Field(default="piece", max_length=20, description="Unit of measurement (e.g., kg, liter, piece)")
    stock_quantity: Optional[int] = Field(default=0, ge=0, description="Current stock quantity")
    is_available: Optional[bool] = Field(default=True, description="Whether the product is available for purchase")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, max_length=50)
    unit: Optional[str] = Field(default=None, max_length=20)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    is_available: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


class AIDescribeRequest(BaseModel):
    """Request body for the AI product description endpoint."""

    name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    price: float = Field(..., gt=0, description="Price of the product in USD")
    category: Optional[str] = Field(
        default="Other",
        max_length=50,
        description="Category of the product (e.g. Produce, Dairy). Defaults to 'Other'.",
    )


class AIDescribeResponse(BaseModel):
    """Response body returned by the AI product description endpoint."""

    description: str = Field(..., description="AI-generated marketing description for the product")
