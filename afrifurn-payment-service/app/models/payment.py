from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class PaymentBase(SQLModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    email: str = Field(..., regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    reference: str = Field(..., unique=True, index=True)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)

class Payment(PaymentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime 