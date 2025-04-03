from dataclasses import dataclass
from typing import Optional

@dataclass
class GetPaymentByReferenceQuery:
    reference: str

@dataclass
class ListPaymentsQuery:
    skip: int = 0
    limit: int = 100
    status: Optional[str] = None
    email: Optional[str] = None 