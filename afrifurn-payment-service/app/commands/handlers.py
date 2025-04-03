from datetime import datetime
import uuid
from fastapi import HTTPException, status
from sqlmodel import Session
from typing import Optional

from models.payment import Payment, PaymentStatus
from services.paynow import PaynowService
from commands.payment_commands import CreatePaymentCommand, UpdatePaymentStatusCommand

class PaymentCommandHandlers:
    def __init__(self, session: Session, paynow_service: PaynowService):
        self.session = session
        self.paynow_service = paynow_service

    async def handle_create_payment(self, command: CreatePaymentCommand) -> Payment:
        # Generate reference if not provided
        reference = command.reference or f"PAY-{uuid.uuid4().hex[:8]}"

        # Create payment record
        payment = Payment(
            amount=command.amount,
            email=command.email,
            currency=command.currency,
            reference=reference,
            status=PaymentStatus.PENDING
        )
        
        self.session.add(payment)
        
        try:
            # Initialize Paynow payment
            paynow_response = await self.paynow_service.create_payment(
                amount=float(command.amount),
                email=command.email,
                reference=reference
            )

            if not paynow_response.success:
                payment.status = PaymentStatus.FAILED
                self.session.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=paynow_response.error or "Payment initialization failed"
                )

            self.session.commit()
            self.session.refresh(payment)

            # Attach Paynow response data
            payment.poll_url = paynow_response.poll_url
            payment.redirect_url = paynow_response.redirect_url

            return payment

        except HTTPException as e:
            raise e
        except Exception as e:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def handle_update_payment_status(self, command: UpdatePaymentStatusCommand) -> Payment:
        payment = self.session.get(Payment, {"reference": command.reference})
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        payment.status = PaymentStatus(command.status)
        payment.updated_at = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(payment)
        
        return payment 