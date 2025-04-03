from abc import ABC,abstractmethod
from dataclasses import dataclass
import decimal

class PaymentStatus:
    PAID="PAID"
    PENDING="PENDING"
    REJECTED="REJECTED"
    
    
@dataclass
class PaymentDetails:
    amount:float
    name:str
    email:str
    currency:str
    pass
@dataclass
class IPaymentService(ABC):
    payment_details:PaymentDetails
    payment_status:str=PaymentStatus.PENDING
    is_paid:bool=False
    @abstractmethod
    def check_payment_status(self):
        pass
    @abstractmethod
    def process_payment(self):
        pass
    
  
class EcoCashPaymentService(IPaymentService):
    
    def check_payment_status(self):
        return "PAID via EcoCash"
    def process_payment(self):
        self.payment_status=PaymentStatus.PENDING
        print("Processing transaction.....",)
        print(f"Status: {self.check_payment_status}",)
        self.payment_status=PaymentStatus.PAID


        print(f"Status: {self.check_payment_status}",)

        return f"Paid {self.payment_details.amount} via Ecocash"
    
    

class ZimswitchPaymentService(IPaymentService):
       def check_payment_status(self):
           
        return self.payment_status
    
       def process_payment(self):
        self.payment_status=PaymentStatus.PENDING
        print("Processing transaction.....",)
        print(f"Status: {self.check_payment_status}",)
        self.payment_status=PaymentStatus.PAID


        print(f"Status: {self.check_payment_status}",)

        return f"Paid {self.payment_details.amount} via Zimswitch"
        