from fastapi import HTTPException, status
from sqlmodel import Session, select
from typing import List

from models.payment import Payment
from queries.payment_queries import GetPaymentByReferenceQuery, ListPaymentsQuery

class PaymentQueryHandlers:
    def __init__(self, session: Session):
        self.session = session

    async def handle_get_payment_by_reference(self, query: GetPaymentByReferenceQuery) -> Payment:
        payment = self.session.exec(
            select(Payment).where(Payment.reference == query.reference)
        ).first()
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        return payment

    async def handle_list_payments(self, query: ListPaymentsQuery) -> List[Payment]:
        statement = select(Payment).offset(query.skip).limit(query.limit)
        
        if query.status:
            statement = statement.where(Payment.status == query.status)
        if query.email:
            statement = statement.where(Payment.email == query.email)
            
        payments = self.session.exec(statement).all()
        return payments 