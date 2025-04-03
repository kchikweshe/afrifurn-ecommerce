from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass
class CreatePaymentCommand:
    email: str

    currency: str = "USD"
    amount: Decimal=0.0
    reference: Optional[str] = None

@dataclass
class UpdatePaymentStatusCommand:
    reference: str
    status: str 