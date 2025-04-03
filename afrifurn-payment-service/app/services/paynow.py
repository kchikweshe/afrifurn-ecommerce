from datetime import time
from paynow import Paynow
from dotenv import load_dotenv
import os

class PaynowService:
    async def create_payment(self, amount: float, email: str, reference: str):
        # Load environment variables
        load_dotenv()
        
        # Initialize Paynow with values from .env
        paynow = Paynow(
            os.getenv('PAYNOW_INTEGRATION_ID'),
            os.getenv('PAYNOW_INTEGRATION_KEY'),
            os.getenv('PAYNOW_RETURN_URL'),
            os.getenv('PAYNOW_RESULT_URL')
        )

        payment = paynow.create_payment('Order', 'kchikweshe@gmail.com')
        payment.add("Payment for Tv Stand",150)

        response = paynow.send_mobile(payment, '0777777777', 'ecocash')
        print("Response==================================",response.data)
        if(response.success):
            poll_url = response.poll_url

        print("Poll Url: ", poll_url)

        status = paynow.check_transaction_status(poll_url)

        time.sleep(30)

        print("Payment Status: ", status.status)


    # async def check_payment_status(self, reference: str):
    #     # Implement status check logic here
    #     if(response.success):
    #         poll_url = response.poll_url

    #     print("Poll Url: ", poll_url)

    #     status = paynow.check_transaction_status(poll_url)

    #     time.sleep(30)

    #     print("Payment Status: ", status.status)
    