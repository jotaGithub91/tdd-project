from datetime import datetime
from decimal import Decimal
from pydantic import UUID4, BaseModel, Field, model_validator, AfterValidator
from store.schemas.base import BaseShemaMixin, OutMixin
from typing import Optional, Annotated
from bson import Decimal128

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")

class ProductIn(ProductBase, BaseShemaMixin):
    ...

class ProductOut(ProductIn, OutMixin):
    ...

def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]

class ProductUpdate(BaseShemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")

class ProductUpdateOut(ProductOut):
    ...