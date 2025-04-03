from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional

from database import get_session
from models.payment import PaymentResponse
from commands.payment_commands import CreatePaymentCommand, UpdatePaymentStatusCommand
from commands.handlers import PaymentCommandHandlers
from queries.payment_queries import GetPaymentByReferenceQuery, ListPaymentsQuery
from queries.handlers import PaymentQueryHandlers
from services.paynow import PaynowService

router = APIRouter(prefix="/payments", tags=["payments"])

def get_command_handlers(session: Session = Depends(get_session)) -> PaymentCommandHandlers:
    return PaymentCommandHandlers(session, PaynowService())

def get_query_handlers(session: Session = Depends(get_session)) -> PaymentQueryHandlers:
    return PaymentQueryHandlers(session)

@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    amount: float,
    email: str,
    currency: str = "USD",
    reference: Optional[str] = None,
    handlers: PaymentCommandHandlers = Depends(get_command_handlers)
):
    command = CreatePaymentCommand(
        amount=amount,
        email=email,
        currency=currency,
        reference=reference
    )
    payment = await handlers.handle_create_payment(command)
    return payment

@router.get("/{reference}", response_model=PaymentResponse)
async def get_payment(
    reference: str,
    handlers: PaymentQueryHandlers = Depends(get_query_handlers)
):
    query = GetPaymentByReferenceQuery(reference=reference)
    return await handlers.handle_get_payment_by_reference(query)

@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    email: Optional[str] = Query(None),
    handlers: PaymentQueryHandlers = Depends(get_query_handlers)
):
    query = ListPaymentsQuery(
        skip=skip,
        limit=limit,
        status=status,
        email=email
    )
    return await handlers.handle_list_payments(query)

@router.post("/webhook")
async def payment_webhook(
    data: dict,
    handlers: PaymentCommandHandlers = Depends(get_command_handlers)
):
    command = UpdatePaymentStatusCommand(
        reference=data.get("reference"),
        status=data.get("status")
    )
    await handlers.handle_update_payment_status(command)
    return {"status": "success"} 